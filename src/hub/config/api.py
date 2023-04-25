from ninja import NinjaAPI
from django.contrib import auth


from core.api import project_router
from core.api import sprint_router
from core.api import task_router


def authenticate(request):
    user = auth.authenticate(
        username=request.headers.get("username"),
        password=request.headers.get("password")
    )
    if user and not user.organization:
        return None
    return user


api = NinjaAPI(auth=authenticate)

api.add_router("/project/", project_router)
api.add_router("/sprint/", sprint_router)
api.add_router("/task/", task_router)
