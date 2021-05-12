import os
import sqlite3

from datasette import hookimpl
from datasette.utils.asgi import Response, NotFound, Forbidden
import sqlite_utils
import uuid


DB_NAME="surveys.db"
DEFAULT_DBPATH="."
TABLE_NAME="surveys"


@hookimpl
def menu_links(datasette, actor):
    async def inner():
        # right now if you have surveys-list permission, we'll show you
        # the menu link which also leads to survey creation (a separate
        # permission
        allowed = await datasette.permission_allowed(
            actor, "surveys-list", default=False
        )
        if allowed:
            return [{
                "href": datasette.urls.path("/-/surveys"),
                "label": "Surveys"
            }]
    return inner


@hookimpl
def register_routes():
    return [
        (r"^/-/surveys$", surveys_list),
        (r"^/-/surveys/new$", surveys_new),
        # link to the specific survey for users to fill (GET & POST)
        (r"^/-/surveys/form/(?P<id>.*)", survey_form),
        (r"^/-/surveys/(?P<id>[0-9a-zA-Z\-]+)", surveys_update),
    ]


def perm_check_maker(datasette, request):
    async def inner_perm_check(*args):
        if not await datasette.permission_allowed(
            request.actor, *args, default=False
        ):
            raise Forbidden("Permission denied")
    return inner_perm_check


def get_db():
    database_path = os.path.join(DEFAULT_DBPATH, f"{DB_NAME}.db")
    return sqlite_utils.Database(sqlite3.connect(database_path))


def get_surveys():
    db = get_db()
    try:
        return db[TABLE_NAME].rows
    except Exception as e:
        print(f"Exception while reading table {TABLE_NAME}: {e}")
        return []


async def surveys_new(scope, receive, datasette, request):
    perm_check = perm_check_maker(datasette, request)
    await perm_check('surveys-create')

    if request.method == "POST":
        formdata = await request.post_vars()
        assert "schema" in formdata, "Invalid POST data"
        assert "options" in formdata, "Invalid POST data"
        schema = formdata["schema"]
        options = formdata["options"]
        survey_id = str(uuid.uuid4())
        db = get_db()
        configs = db[TABLE_NAME]
        configs.insert({
            "id": survey_id,
            "schema": schema,
            "options": options,
        }, pk="id", replace=True)
        return Response.redirect(
            f"/-/surveys/{survey_id}"
        )

    return Response.html(
        await datasette.render_template(
            "form-builder.html", {
                "id": "new",
            }, request=request
        )
    )


async def surveys_update(scope, receive, datasette, request):
    perm_check = perm_check_maker(datasette, request)
    await perm_check('surveys-create')
    survey_id = request.url_vars["id"]
    assert survey_id, "Survey ID missing"

    db = get_db()
    configs = db[TABLE_NAME]

    if request.method == "POST":
        formdata = await request.post_vars()
        assert "schema" in formdata, "Invalid POST data"
        assert "options" in formdata, "Invalid POST data"
        schema = formdata["schema"]
        options = formdata["options"]
        configs.insert({
            "id": survey_id,
            "schema": schema,
            "options": options,
        }, pk="id", replace=True)
        # TODO: generate save message?

    survey_data = configs.get(survey_id)
    assert survey_data, "Survey not found."

    return Response.html(
        await datasette.render_template(
            "form-builder.html", {
                "id": survey_id,
                "schema": survey_data["schema"],
                "options": survey_data["options"],
            }, request=request
        )
    )



async def surveys_list(scope, receive, datasette, request):
    perm_check = perm_check_maker(datasette, request)
    await perm_check('surveys-list')

    return Response.html(
        await datasette.render_template(
            "surveys-list.html", {
                "surveys": get_surveys()
            }, request=request
        )
    )


async def surveys(scope, receive, datasette, request):
    perm_check = perm_check_maker(datasette, request)
    try:
        survey_id = request.url_vars["id"]
    except KeyError:
        survey_id = None

    # CREATE
    if request.method == "POST":
        await perm_check('surveys-create')
        raise NotImplementedError("Didn't write it yet")

    elif request.method == "PUT":
        await perm_check('surveys-update', survey_id)

    elif request.method == "DELETE":
        await perm_check('surveys-delete', survey_id)
        return Response.html(
            await datasette.render_template(
                "deleted.html", {
                    "survey": {}
                }, request=request
            )
        )

    # GET - LIST surveys
    # TODO: piggyback off of a normal datasette list view thing - clicking
    # brings you to the editor, same as add new button does
    assert request.method == "GET", f"Method {request.method} not supported"
    await perm_check('surveys-list')

    return Response.html(
        await datasette.render_template(
            "surveys-list.html", {
                "surveys": []
            }, request=request
        )
    )


async def survey_form(scope, receive, datasette, request):
    survey_id = request.url_vars["id"]

    perm_check = perm_check_maker(datasette, request)
    await perm_check('surveys-view-form', survey_id)

    db = get_db()
    configs = db[TABLE_NAME]
    cfg = configs.get(survey_id)
    if not cfg:
        raise NotFound(f"Form not found: {survey_id}")

    return Response.html(
        await datasette.render_template(
            "form.html", {
                "schema": cfg["schema"],
                "options": cfg["options"],
                "id": survey_id,
            }, request=request
        )
    )
