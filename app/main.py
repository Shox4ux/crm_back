from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from .src.warehouse import warehouse_router
from .src.product import product_router
from .src.admin import admin_router
from .src.client import client_router
from .src.user import user_router


from .src.auth import auth_router
from .utils.custom_exceptions import global_exception_handler


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")


@app.get("/")
async def main():
    return "We are creating crm project here"


app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(client_router.router)
app.include_router(user_router.router)
app.include_router(warehouse_router.router)
app.include_router(product_router.router)
