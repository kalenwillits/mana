from ninja import NinjaAPI

from core.api.sync import router as sync_router

api = NinjaAPI()

api.add_router("/sync/", sync_router)
