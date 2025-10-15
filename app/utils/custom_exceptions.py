from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# from app.exceptions import WarehouseNotFoundError, ProductAlreadyExistsError


async def global_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, ItemNotFound):
        return JSONResponse(status_code=404, content={"message": exc.message})

    if isinstance(exc, AuthError):
        return JSONResponse(
            status_code=exc.code,
            content={"message": exc.message},
            headers=exc.headers,
        )
    else:
        data: dict = {"message": "System error"}
        return JSONResponse(status_code=500, content=data)


class ItemNotFound(Exception):
    def __init__(self, item_id: int, item: str):
        self.item_id = item_id
        self.message = f"{item.upper()} with id {item_id} not found."
        super().__init__(self.message)


class AuthError(Exception):
    def __init__(self):
        self.code = 401
        self.message = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(self.message, self.code, self.headers)
