from uuid import UUID
from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Project
from core.models import State
from core.models import Sprint
from core.models import Task
from core.models import Log

from core.schemas import ProjectIn
from core.schemas import SprintIn


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


@router.post("/use/project/")
def use_project(request, name: str):
    user = request.auth
    project = get_object_or_404.NOT_FOUND(Project, organization=user.organization, name=name)
    user.project = project
    user.save()
    return HTTPStatus.ACCEPTED


@router.post("/use/sprint/")
def use_sprint(request, name: str):
    user = request.auth
    sprint = get_object_or_404.NOT_FOUND(Sprint, organization=user.organization, name=name)
    user.sprint = sprint
    user.save()
    return HTTPStatus.ACCEPTED


@router.post("/use/task/")
def use_task(request, name: str):
    user = request.auth
    task = get_object_or_404.NOT_FOUND(Task, organization=user.organization, name=name)
    user.task = task
    user.save()
    return HTTPStatus.ACCEPTED


@router.post("/new/project/")
def new_project(request, payload: ProjectIn):
    user = request.auth
    project = Project(
        organization=user.organization,
        **payload.dict()
    )
    project.save()
    return HTTPStatus.CREATED


@router.post("/new/sprint/")
def new_sprint(request, payload: SprintIn):
    user = request.auth
    sprint = Sprint(
        organization=user.organization,
        **payload.dict()
    )
    sprint.save()
    return HTTPStatus.CREATED



@router.post("/set/project/", response={HTTPStatus.CREATED: type(None), HTTPStatus.NOT_FOUND: type(None)})
def set_project(request, state_name: str):
    user = request.auth
    if not user.project:
        return 400
    state = get_object_or_404.NOT_FOUND(State, organization=user.organization, name=state_name)
    user.project.state = state
    user.project.save()
    return HTTPStatus.CREATED


@router.get("/status/project/", response={HTTPStatus.OK: dict, HTTPStatus.NOT_FOUND: type(None)})
def get_project_status(request):
    user = request.auth
    response = []
    return HTTPStatus.OK, response


@router.get("/pull/", response={HTTPStatus.OK: dict, 400: type(None)})
def pull(request):
    user = request.auth
    if not user.project:
        return 400
    return HTTPStatus.OK, Project.objects.hydrate(id=user.project.id)


@router.post("/push/", response={HTTPStatus.CREATED: type(None)})
def push(request, payload: dict):
    user = request.auth
    project = Project
    return HTTPStatus.CREATED
