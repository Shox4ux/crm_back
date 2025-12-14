from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request
from .src.warehouse import warehouse_router
from .src.product import product_router
from .src.admin import admin_router
from .src.client import client_router
from .src.user import user_router
from .src.order import order_router
from .src.order_product import order_product_router
from .src.warehouse_product import warehouse_product_router
from .src.product_expense import product_expense_router
from .src.auth import auth_router
from .utils.custom_exceptions import global_exception_handler
from app.settings import Settings
import subprocess
import hmac
import hashlib
import os

settings = Settings()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)

app.mount(
    "/uploads", StaticFiles(directory=settings.ASSETS_FOLDER_PATH), name="uploads"
)


@app.get("/")
async def main():
    return "We are creating crm project here"


GITHUB_SECRET = b"SUPER_SECRET_STRING"


def verify_signature(payload_body, signature_header):
    mac = hmac.new(GITHUB_SECRET, msg=payload_body, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature_header)


# lets try this code
@app.post("/deploy")
async def deploy(request: Request):
    signature = request.headers.get("X-Hub-Signature-256")
    body = await request.body()
    if not signature or not verify_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    subprocess.Popen(["/root/crm_back/deploy.sh"])
    return {"status": "deploy started"}


app.include_router(auth_router.router)
app.include_router(user_router.router)

app.include_router(admin_router.router)
app.include_router(client_router.router)
app.include_router(product_router.router)
app.include_router(product_expense_router.router)

app.include_router(warehouse_router.router)
app.include_router(warehouse_product_router.router)

app.include_router(order_router.router)
app.include_router(order_product_router.router)
