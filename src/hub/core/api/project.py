from http import HTTPStatus
from datetime import datetime

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Project
from core.models import State
from core.models import Log
from core.models import Comment
from core.schemas import UseProjectIn
from core.schemas import NewProjectIn
from core.schemas import PushProjectIn
from core.schemas import SetProjectIn
from core.schemas import DropProjectIn
from core.schemas import PullProjectOut
from core.schemas import PullCommentOut


router = Router()


@router.put("/use/", response={
        HTTPStatus.ACCEPTED: dict
    }
)
def use(request, payload: UseProjectIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    old_project = user.project
    name = Project.normalize_str(payload.name)
    instance = get_object_or_404(
        Project,
        organization=user.organization,
        name=name
    )
    instance.read_at = timestamp
    user.project = instance
    user.save()
    Log(
        organization=user.organization,
        info=f"use [{old_project}] -> [{user.project}]",
        user=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": "Project selected."}


@router.post("/new/", response={
        HTTPStatus.CREATED: dict,
        HTTPStatus.CONFLICT: dict
    }
)
def new(request, payload: NewProjectIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if Project.objects.filter(organization=user.organization, name=Project.normalize_str(payload.name)).exists():
        return HTTPStatus.CONFLICT, {"detail": f"Project [{payload.name}] already exists."}
    instance = Project(
        organization=user.organization,
        owner=user.role
    ).update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"new [{instance}]",
        user=user,
        link=instance,
    ).save()

    return HTTPStatus.CREATED, {"detail": "Project created."}


@router.put("/set/", response={
        HTTPStatus.ACCEPTED: dict,
        HTTPStatus.BAD_REQUEST: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def set(request, payload: SetProjectIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    old_state = user.project.state
    name = State.normalize_str(payload.state)
    state = get_object_or_404(
        State,
        organization=user.organization,
        name=name,
    )
    state.read_at = timestamp
    if state.role != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    user.project.state = state
    user.project.updated_at = timestamp
    user.project.save()
    Log(
        organization=user.organization,
        info=f"set [{old_state}] -> [{state}]",
        user=user,
        link=user.project,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": f"[{user.project}] set [{payload.state}]."}


@router.delete("/drop/", response={
        HTTPStatus.OK: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def drop(request, payload: DropProjectIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.updated_at = timestamp
    user.save()
    name = State.normalize_str(payload.name)
    instance = get_object_or_404(Project, organization=user.organization, name=name)
    if instance.owner != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    instance.delete()
    Log(
        organization=user.organization,
        info=f"drop [{instance}]",
        user=user,
        link=None,
    ).save()
    return HTTPStatus.OK, {"detail": "Project deleted."}


@router.put("/push/", response={
        HTTPStatus.ACCEPTED: dict,
        HTTPStatus.BAD_REQUEST: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def push(request, payload: PushProjectIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    instance = get_object_or_404(
        Project,
        organization=user.organization,
        id=user.project.id
    )
    if instance.owner != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    instance.updated_at = timestamp
    instance.update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"push [{instance}]",
        user=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": "Project changes accepted."}


@router.get("/pull/", response={
        HTTPStatus.OK: PullProjectOut,
        HTTPStatus.BAD_REQUEST: dict
    }
)
def pull(request):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    project_queryset = Project.objects.filter(
        organization=user.organization, id=user.project.id
    )
    project_comment_queryset = Comment.objects.filter(
        organization=user.organization,
        project=user.project
    ).order_by("created_at")
    project_queryset.update(read_at=timestamp)
    project_comment_queryset.update(read_at=timestamp)
    Log(
        organization=user.organization,
        info=f"pull project [{user.project}]",
        user=user,
        link=project_queryset.first(),
    ).save()
    response = project_queryset.values(*PullProjectOut.fields()).first()
    response["comments"] = list(project_comment_queryset.values(*PullCommentOut.fields()))
    return HTTPStatus.OK, response
