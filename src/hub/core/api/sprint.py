from http import HTTPStatus
from datetime import datetime

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Sprint
from core.models import State
from core.models import Log
from core.models import Comment
from core.schemas import UseSprintIn
from core.schemas import NewSprintIn
from core.schemas import PushSprintIn
from core.schemas import SetSprintIn
from core.schemas import DropSprintIn
from core.schemas import PullSprintOut
from core.schemas import PullCommentOut


router = Router()


@router.put("/use/", response={
        HTTPStatus.ACCEPTED: dict
    }
)
def use(request, payload: UseSprintIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    old_sprint = user.sprint
    name = Sprint.normalize_str(payload.name)
    instance = get_object_or_404(
        Sprint,
        organization=user.organization,
        name=name
    )
    instance.read_at = timestamp
    user.sprint = instance
    user.save()
    Log(
        organization=user.organization,
        info=f"use [{old_sprint}] -> [{user.sprint}]",
        user=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": "Sprint selected."}


@router.post("/new/", response={
        HTTPStatus.CREATED: dict,
        HTTPStatus.CONFLICT: dict
    }
)
def new(request, payload: NewSprintIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if Sprint.objects.filter(organization=user.organization, name=Sprint.normalize_str(payload.name)).exists():
        return HTTPStatus.CONFLICT, {"detail": f"Sprint [{payload.name}] already exists."}
    instance = Sprint(
        organization=user.organization,
        owner=user.role
    ).update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"new [{instance}]",
        user=user,
        link=instance,
    ).save()

    return HTTPStatus.CREATED, {"detail": "Sprint created."}


@router.put("/set/", response={
        HTTPStatus.ACCEPTED: dict,
        HTTPStatus.BAD_REQUEST: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def set(request, payload: SetSprintIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.sprint:
        return HTTPStatus.BAD_REQUEST, {"detail": "No sprint in use."}
    old_state = user.sprint.state
    name = State.normalize_str(payload.state)
    state = get_object_or_404(
        State,
        organization=user.organization,
        name=name,
    )
    state.read_at = timestamp
    if state.role != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    user.sprint.state = state
    user.sprint.updated_at = timestamp
    user.sprint.save()
    Log(
        organization=user.organization,
        info=f"set [{old_state}] -> [{state}]",
        user=user,
        link=user.sprint,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": f"[{user.project}] set [{payload.state}]."}


@router.delete("/drop/", response={
        HTTPStatus.OK: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def drop(request, payload: DropSprintIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.updated_at = timestamp
    user.save()
    name = State.normalize_str(payload.name)
    instance = get_object_or_404(Sprint, organization=user.organization, name=name)
    if instance.owner != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    instance.delete()
    Log(
        organization=user.organization,
        info=f"drop [{instance}]",
        user=user,
        link=None,
    ).save()
    return HTTPStatus.OK, {"detail": "Sprint deleted."}


@router.put("/push/", response={
        HTTPStatus.ACCEPTED: dict,
        HTTPStatus.BAD_REQUEST: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def push(request, payload: PushSprintIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.sprint:
        return HTTPStatus.BAD_REQUEST, {"detail": "No sprint in use."}
    instance = get_object_or_404(
        Sprint,
        organization=user.organization,
        id=user.sprint.id
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
    return HTTPStatus.ACCEPTED, {"detail": "Sprint changes accepted."}


@router.get("/pull/", response={
        HTTPStatus.OK: PullSprintOut,
        HTTPStatus.BAD_REQUEST: dict
    }
)
def pull(request):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.sprint:
        return HTTPStatus.BAD_REQUEST, {"detail": "No sprint in use."}
    sprint_queryset = Sprint.objects.filter(
        organization=user.organization, id=user.sprint.id
    )
    sprint_comment_queryset = Comment.objects.filter(
        organization=user.organization,
        sprint=user.sprint
    )
    sprint_queryset.update(read_at=timestamp).save()
    sprint_comment_queryset.update(read_at=timestamp).save()
    Log(
        organization=user.organization,
        info=f"pull sprint [{user.sprint}]",
        user=user,
        link=sprint_queryset.first(),
    ).save()
    response = sprint_queryset.values(*PullSprintOut.fields()).first()
    response["comments"] = list(sprint_comment_queryset.values(*PullCommentOut.fields()))
    return HTTPStatus.OK, response
