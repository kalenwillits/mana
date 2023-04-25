from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Project
from core.models import Sprint
from core.models import State
from core.models import Task
from core.models import Log
from core.schemas import UseProjectIn
from core.schemas import NewProjectIn
from core.schemas import PushProjectIn
from core.schemas import SetProjectIn
from core.schemas import DropProjectIn
from core.schemas import PullProjectOut
from core.schemas import PullSprintOut
from core.schemas import PullTaskOut


router = Router()


@router.put("/use/", response={HTTPStatus.ACCEPTED: dict})
def use(request, payload: UseProjectIn):
    user = request.auth
    old_project = user.user.project
    name = Project.normalize_str(payload.name)
    instance = get_object_or_404(Project, organization=user.organization, name=name)
    user.project = instance
    user.save()
    Log(
        organization=user.organization,
        info=f"use [{old_project}] -> [{user.project}]",
        owner=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": f"Project [{instance.name}] selected."}


@router.post("/new/", response={HTTPStatus.CREATED: dict, HTTPStatus.CONFLICT: dict})
def new(request, payload: NewProjectIn):
    user = request.auth
    if Project.objects.filter(organization=user.organization, name=Project.normalize_str(payload.name)).exists():
        return HTTPStatus.CONFLICT, {"detail": f"Project [{payload.name}] already exists."}
    instance = Project(organization=user.organization).update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"new [{user.project}]",
        owner=user,
        link=instance,
    ).save()

    return HTTPStatus.CREATED, {"detail": "Project created."}


@router.put("/set/", response={HTTPStatus.ACCEPTED: dict, HTTPStatus.BAD_REQUEST: dict})
def set(request, payload: SetProjectIn):
    user = request.auth
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    old_state = user.project.state
    name = State.normalize_str(payload.state)
    state = get_object_or_404(State, organization=user.organization, name=name)
    user.project.state = state
    user.project.save()
    Log(
        organization=user.organization,
        info=f"set [{old_state}] -> [{state}]",
        owner=user,
        link=user.project,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": f"[{user.project.name}] set [{payload.state}]."}


@router.delete("/drop/", response={HTTPStatus.OK: dict})
def drop(request, payload: DropProjectIn):
    user = request.auth
    name = State.normalize_str(payload.name)
    instance = get_object_or_404(Project, organization=user.organization, name=name)
    instance.delete()
    Log(
        organization=user.organization,
        info=f"drop [{instance}]",
        owner=user,
        link=None,
    ).save()
    return HTTPStatus.OK, {"detail": "Project deleted."}


@router.put("/push/", response={HTTPStatus.ACCEPTED: dict, HTTPStatus.BAD_REQUEST: dict})
def push(request, payload: PushProjectIn):
    user = request.auth
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    instance = get_object_or_404(
        Project,
        organization=user.organization,
        id=user.project.id
    ).update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"push [{instance}]",
        owner=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": "Project changes accepted."}


@router.get("/pull/", response={HTTPStatus.OK: PullProjectOut, HTTPStatus.BAD_REQUEST: dict})
def pull(request):
    user = request.auth
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    response = Project.objects.filter(
        organization=user.organization, id=user.project.id
    ).values(*PullProjectOut.fields()).first()

    response["sprints"] = list(Sprint.objects.filter(
        organization=user.organization,
        project=user.project
    ).values(*PullSprintOut.fields()))

    for sprint in response["sprints"]:
        sprint["tasks"] = list(Task.objects.filter(
            organization=user.organization,
            sprint=user.sprint,
            asignee=user
        ).values(*PullTaskOut.fields()))

    Log(
        organization=user.organization,
        info=f"pull [{user.project}]",
        owner=user,
        link=user.project,
    ).save()
    return HTTPStatus.OK, response
