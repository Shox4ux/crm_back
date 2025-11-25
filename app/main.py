from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, Request
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


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)

app.mount("/uploads", StaticFiles(directory="/home/ubuntu/uploads"), name="uploads")

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     # Read and clone the body (you can only read it once)
#     body = await request.body()
#     try:
#         body_data = json.loads(body.decode("utf-8"))
#     except Exception:
#         body_data = body.decode("utf-8") if body else None

#     print(f"\n➡️  {request.method} {request.url.path}")
#     if body_data:
#         print(f"📦 Body: {json.dumps(body_data, indent=2, ensure_ascii=False)}")
#     else:
#         print("📭 Empty body")

#     # Call the actual endpoint
#     response = await call_next(request)
#     print(f"⬅️  Response status: {response.status_code}\n")

#     return response


@app.get("/")
async def main():
    return "We are creating crm project here"


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
