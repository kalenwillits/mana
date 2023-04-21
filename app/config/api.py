from ninja import NinjaAPI
from django.contrib import auth


from core.api.project import router as project_router


def authenticate(request):
    return auth.authenticate(
        username=request.headers.get("username"),
        password=request.headers.get("password")
    )


api = NinjaAPI(auth=authenticate)

api.add_router("/project/", project_router)
