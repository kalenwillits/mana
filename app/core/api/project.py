from uuid import UUID

from ninja import Router

from core.models.project import Project


router = Router()


@router.get("/", response={200: list, 400: type(None), 403: type(None)})
def get_project(request, project_id: UUID = None):
    user = request.auth
    filters = {}

    if not user.organization:
        return 400, None

    if project_id:
        filters["project_id"] = project_id
    response = Project.objects.hydrate(organization=user.organization, **filters)
    return 200, response
