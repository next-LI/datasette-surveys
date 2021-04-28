from datasette import hookimpl
from datasette.utils.asgi import Response, NotFound, Forbidden


@hookimpl
def permission_allowed(actor, action):
    if action.startswith("surveys-") and actor and actor.get("id") == "root":
        return True


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
        # full CRUD for surveys (ADMIN ONLY)
        (r"^/-/surveys/(?P<id>.*)/?$", surveys),
        # link to the specific survey for users to fill (GET & POST)
        (r"^/-/surveys/form/(?P<id>.*)/?$", survey_form),
    ]



def perm_check_maker(datasette, request):
    async def inner_perm_check(perm):
        if not await datasette.permission_allowed(
            request.actor, perm, default=False
        ):
            raise Forbidden("Permission denied")
    return inner_perm_check


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

    if request.method == "PUT":
        await perm_check('surveys-update', survey_id)

    elif request.method == "DELETE":
        await perm_check('surveys-delete', survey_id)
        return Response.html(
            await datasette.render_template(
                "deleted.html", {
                    "survey": {}
                },
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
            },
        )
    )


async def survey_edit(scope, receive, datasette, request):
    return Response.html(
        await datasette.render_template(
            "surveys-.html", {
                "surveys": []
            },
        )
    )


async def survey_form(scope, receive, datasette, request):
    survey_id = request.url_vars["id"]
    perm_check = perm_check_maker(datasette, request)
    await perm_check('surveys-view-form', survey_id)
    return Response.html(
        await datasette.render_template(
            "surveys-form.html", {
                "schema": {},
                "survey_id": survey_id,
            },
        )
    )
