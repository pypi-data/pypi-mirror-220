import cProfile
import csv
import io
import json
import marshal
import pstats
import sys
from collections import defaultdict

import django.contrib.admin.views.decorators as admin_decorators
import hyperlink
import sqlparse
from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404
from django.template import engines, loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators import csrf

from . import version
from .common import (
    PUBLIC_PERM,
    SHARE_PERM,
    HttpResponse,
    JsonResponse,
    global_state,
    has_permission,
    set_global_state,
    settings,
)
from .format_csv import get_csv_rows
from .models import View
from .orm_results import get_result_list, get_result_queryset, get_results
from .query import BoundQuery, Query, QueryFilter
from .types import TYPES
from .util import str_to_field


def _get_query_data(bound_query):
    return {
        "filters": [
            {
                "pathStr": filter_.path_str,
                "lookup": filter_.lookup,
                "value": filter_.value,
                "errorMessage": filter_.error_message,
                "parsed": filter_.formatted_value(),
            }
            for filter_ in bound_query.filters
        ],
        "fields": [
            {
                "pathStr": field.path_str,
                "sort": field.direction,
                "priority": field.priority,
                "pivoted": field.pivoted,
                "errorMessage": field.error_message,
            }
            for field in bound_query.fields
        ],
        "model": bound_query.model_name,
        "limit": bound_query.limit,
    }


def _get_model_fields(model_name, orm_models):
    orm_model = orm_models[model_name]

    def sort_model_fields(fields):
        front = {
            orm_model.pk: 1,
            str_to_field(settings.DATA_BROWSER_ADMIN_FIELD_NAME.lower()): 2,
        }
        sorted_fields = sorted(
            fields.items(),
            key=lambda name_field: (
                front.get(name_field[0], sys.maxsize),
                name_field[1]["prettyName"],
            ),
        )
        return [name for name, field in sorted_fields]

    all_fields = {
        name: {
            "model": orm_field.rel_name,
            "toMany": orm_field.to_many,
            "type": orm_field.type_.name if orm_field.type_ else None,
            "concrete": orm_field.concrete,
            "canPivot": orm_field.can_pivot,
            "prettyName": orm_field.pretty_name,
            "choices": [v for k, v in orm_field.choices],
            "defaultSort": orm_field.default_sort,
            "actions": [
                {"name": name, "prettyName": desc}
                for name, (func, desc) in sorted((orm_field.actions or {}).items())
            ],
        }
        for name, orm_field in orm_model.fields.items()
    }

    q = Query(model_name, [], [QueryFilter(*f) for f in orm_model.default_filters])
    bq = BoundQuery.bind(q, orm_models)

    return {
        "fields": all_fields,
        "sortedFields": sort_model_fields(all_fields),
        "defaultFilters": [
            {
                "pathStr": filter_.path_str,
                "lookup": filter_.lookup,
                "value": filter_.value,
            }
            for filter_ in bq.filters
        ],
    }


def _get_config():
    orm_models = global_state.models
    types = {
        name: {
            "lookups": {
                n: {"prettyName": tn, "type": t}
                for n, (tn, t, _) in type_.lookups.items()
            },
            "sortedLookups": list(type_.lookups),
            "defaultLookup": type_.default_lookup,
            "defaultValue": type_.default_value,
        }
        for name, type_ in TYPES.items()
    }

    all_model_fields = {
        model_name: _get_model_fields(model_name, orm_models)
        for model_name in orm_models
    }

    model_names_by_app = defaultdict(set)
    for name, model in orm_models.items():
        if model.root:
            # TODO why don't we get this in parts and then assemble it
            app_name, model_name = name.split(".")
            model_names_by_app[app_name].add(model_name)

    return {
        "baseUrl": reverse("data_browser:home"),
        "types": types,
        "allModelFields": all_model_fields,
        "sortedModels": [
            {"appName": app_name, "modelNames": sorted(model_names)}
            for app_name, model_names in sorted(model_names_by_app.items())
        ],
        "canMakePublic": has_permission(global_state.request.user, PUBLIC_PERM),
        "canShare": has_permission(global_state.request.user, SHARE_PERM),
        "sentryDsn": settings.DATA_BROWSER_FE_DSN,
        "defaultRowLimit": settings.DATA_BROWSER_DEFAULT_ROW_LIMIT,
        "appsExpanded": settings.DATA_BROWSER_APPS_EXPANDED,
    }


@admin_decorators.staff_member_required
@set_global_state(public_view=False)
def query_ctx(request, *, model_name="", fields=""):
    config = _get_config()
    return JsonResponse(config)


def admin_action(request, model_name, fields):
    data = json.loads(request.body)
    action = data["action"]
    field = data["field"]

    if field not in fields:
        raise http.Http404(f"bad field '{field}'")  # pragma: no cover

    params = hyperlink.parse(request.get_full_path()).query
    query = Query.from_request(model_name, fields, params)

    orm_models = global_state.models
    if query.model_name not in orm_models:
        raise http.Http404(f"'{query.model_name}' does not exist")  # pragma: no cover

    bound_query = BoundQuery.bind(query, orm_models)
    idx = [field.path_str for field in bound_query.fields].index(field)
    bound_field = bound_query.fields[idx].orm_bound_field

    if not bound_field.field.actions or action not in bound_field.field.actions:
        raise http.Http404(f"bad action '{action}'")  # pragma: no cover

    results = get_result_list(bound_query)

    pks = {row[bound_field.queryset_path_str] for row in results}
    pks -= {None}

    model_name = bound_field.field.model_name
    return orm_models[model_name].get_http_request_for_action(action, pks)


@csrf.csrf_protect
@csrf.ensure_csrf_cookie
@admin_decorators.staff_member_required
@set_global_state(public_view=False)
def query_html(request, *, model_name="", fields=""):
    if request.method == "POST":
        return admin_action(request, model_name, fields)

    config = _get_config()
    config = json.dumps(config, cls=DjangoJSONEncoder)
    config = (
        config.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")
    )

    if settings.DATA_BROWSER_DEV:  # pragma: no cover
        try:
            response = _get_from_js_dev_server(request, "get")
        except Exception as e:
            return HttpResponse(f"Error loading from JS dev server.<br><br>{e}")

        template = engines["django"].from_string(response.text)
    else:
        template = loader.get_template("data_browser/index.html")

    return TemplateResponse(request, template, {"config": config, "version": version})


@admin_decorators.staff_member_required
@set_global_state(public_view=False)
def query(request, *, model_name, fields="", media):
    params = hyperlink.parse(request.get_full_path()).query

    if media.startswith("profile") or media.startswith("pstats"):
        if "_" in media:
            prof_media, media = media.split("_")
        else:
            prof_media = media
            media = "json"

        profiler = cProfile.Profile()
        try:
            profiler.enable()

            query = Query.from_request(model_name, fields, params)
            for x in _data_response(query, media, privileged=True):
                pass

            profiler.disable()

            if prof_media == "profile":
                buffer = io.StringIO()
                stats = pstats.Stats(profiler, stream=buffer)
                stats.sort_stats("cumulative").print_stats(50)
                stats.sort_stats("time").print_stats(50)
                buffer.seek(0)
                return HttpResponse(buffer, content_type="text/plain")
            elif prof_media == "pstats":
                buffer = io.BytesIO()
                marshal.dump(pstats.Stats(profiler).stats, buffer)
                buffer.seek(0)
                response = HttpResponse(buffer, content_type="application/octet-stream")
                response["Content-Disposition"] = (
                    "attachment;"
                    f" filename={query.model_name}-{timezone.now().isoformat()}.pstats"
                )
                return response
            else:
                raise http.Http404(f"Bad file format {prof_media} requested")
        finally:
            if profiler:  # pragma: no branch
                profiler.disable()
    else:
        query = Query.from_request(model_name, fields, params)
        return _data_response(query, media, privileged=True)


def view(request, pk, media):
    view = get_object_or_404(View.objects.filter(public=True), public_slug=pk)
    with set_global_state(request=request, user=view.owner, public_view=True):
        if (
            # some of these are checked by the admin but this is a good time to be paranoid
            view.owner
            and view.owner.is_active
            and view.owner.is_staff
            and has_permission(view.owner, PUBLIC_PERM)
            and settings.DATA_BROWSER_ALLOW_PUBLIC
            and view.is_valid()
        ):
            query = view.get_query()
            return _data_response(query, media, privileged=False)
        else:
            raise http.Http404("No View matches the given query.")


class Echo:
    def write(self, value):
        return value


def _data_response(query, media, privileged=False):
    orm_models = global_state.models
    if query.model_name not in orm_models:
        raise http.Http404(f"{query.model_name} does not exist")
    bound_query = BoundQuery.bind(query, orm_models)

    if media == "csv":
        results = get_results(bound_query, orm_models, False)
        csv_rows = get_csv_rows(bound_query, results)

        writer = csv.writer(Echo())
        response = http.StreamingHttpResponse(
            (writer.writerow(row) for row in csv_rows), content_type="text/csv"
        )
        response["Content-Disposition"] = (
            f"attachment; filename={query.model_name}-{timezone.now().isoformat()}.csv"
        )
        return response
    elif media == "json":
        results = get_results(bound_query, orm_models, True)
        resp = _get_query_data(bound_query) if privileged else {}
        resp.update(results)
        return JsonResponse(resp)
    elif privileged and media == "query":
        resp = _get_query_data(bound_query)
        return JsonResponse(resp)
    elif privileged and media in ["sql", "explain", "analyze", "qs"]:
        query_set = get_result_queryset(bound_query, media == "qs")
        if isinstance(query_set, list):
            res = "Not available for pure aggregates"
        else:
            # disclaimer
            if media in ["sql", "explain", "analyze"]:
                res = (
                    "/* This is an approximation of the main query.\nPages with pivoted"
                    " or calculated data may do additional queries. */\n\n\n"
                )
            elif media == "qs":
                res = (
                    "# This is an approximation of the main queryset.\n# Pages with"
                    " pivoted or calculated data may do additional queries.\n\n\n"
                )
            else:
                assert False

            # main part
            if media == "sql":
                pass  # actual SQL is handled below
            elif media == "explain":
                res += query_set.explain()
                res += "\n\n\n"
            elif media == "analyze":
                res += query_set.explain(analyze=True)
                res += "\n\n\n"
            elif media == "qs":
                res += str(query_set)
            else:
                assert False

            # sql
            if media in ["sql", "explain", "analyze"]:
                res += sqlparse.format(
                    str(query_set.query), reindent=True, keyword_case="upper"
                )
        return HttpResponse(res, content_type="text/plain")
    else:
        raise http.Http404(f"Bad file format {media} requested")


def _get_from_js_dev_server(request, method=None):  # pragma: no cover
    import requests

    if method is None:
        method = request.META["REQUEST_METHOD"].lower()

    upstream_url = f"http://127.0.0.1:3000{request.path}"
    sys.stdout.write(f"Proxy request: {method} {upstream_url}\n")
    return getattr(requests, method)(upstream_url, stream=True)


@csrf.csrf_exempt
def proxy_js_dev_server(request, path):  # pragma: no cover
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    response = _get_from_js_dev_server(request)
    return http.StreamingHttpResponse(
        streaming_content=response.iter_content(2**12),
        content_type=response.headers.get("Content-Type"),
        status=response.status_code,
        reason=response.reason,
    )
