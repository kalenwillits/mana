from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Project
from core.models import State
from core.models import Log


router = Router()


__scratch_client_commands__ = """
mana set project todo

mana use project user-menus
or
mana use pro "user menus"
or
mana use p user_menus

# Make spaces and underscores are equivelent.



mana new p [project name]
mana new t [task name] (must be using current project & sprint)



mana init (Installs global mana configuration into project)


"""


@router.post("/use/project/", response={201: type(None), 404: type(None)})
def use_project(request, project_name: str):
    user = request.auth
    project = get_object_or_404(Project, organization=user.organization, name=project_name)
    user.project = project
    user.save()
    return 201


# @router.post("/use/sprint/")


# @router.post("/use/task/")


@router.post("/set/project/", response={201: type(None), 404: type(None)})
def set_project(request, state_name: str):
    user = request.auth
    if not user.project:
        return 400
    state = get_object_or_404(State, organization=user.organization, name=state_name)
    user.project.state = state
    user.project.save()
    return 201


@router.get("/status/project/", response={200: dict, 404: type(None)})
def get_project_status(request):
    user = request.auth
    response = []
    return 200, response


@router.get("/pull/", response={200: dict, 400: type(None)})
def pull(request):
    user = request.auth
    if not user.project:
        return 400
    return 200, Project.objects.hydrate(id=user.project.id)


@router.post("/push/", response={201: type(None)})
def push(request, payload: dict):
    user = request.auth
    project = Project
    return 201
