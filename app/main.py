from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from .src.warehouse.router import router as warehouse_router
from .src.product.router import router as product_router
from .src.admin.router import router as admin_router
from .src.client.router import router as client_router
from .src.user.router import router as user_router
from .src.order.router import router as order_router
from .src.order_product.router import router as order_product_router
from .src.warehouse_product.router import router as warehouse_product_router
from .src.product_expense.router import router as product_expense_router
from .src.auth.router import router as auth_router
from app.settings import Settings


settings = Settings()


app = FastAPI(
    title="CRM API",
    description="API for CRM project",
    version="0.0.1",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_exception_handler(Exception, global_exception_handler)

app.mount(
    "/uploads", StaticFiles(directory=settings.ASSETS_FOLDER_PATH), name="uploads"
)


@app.get("/")
async def main():
    return "We are creating crm project here"


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(product_expense_router)
app.include_router(warehouse_router)
app.include_router(warehouse_product_router)
app.include_router(order_router)
app.include_router(order_product_router)
