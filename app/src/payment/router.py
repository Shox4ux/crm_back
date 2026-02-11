from typing import Optional
from fastapi import APIRouter, status, Depends
from app.utils.custom_exceptions import ItemNotFound
from .dao import PaymentDao, get_pay_dao
from app.src.payment.schema import PaymentResponse, PaymentCreate, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["payment"])


@router.get("/get_all", response_model=Optional[list[PaymentResponse]])
async def get_all_payments(dao: PaymentDao = Depends(get_pay_dao)):
    payments = await dao.get_all()
    return payments


@router.get("/get_by_id/{id}", response_model=PaymentResponse)
async def get_payment_by_id(id: int, dao: PaymentDao = Depends(get_pay_dao)):
    payment = await dao.get_by_id(id)
    if not payment:
        raise ItemNotFound(item="payment", item_id=id)
    return payment


@router.post("/create")
async def create_payment(data: PaymentCreate, dao: PaymentDao = Depends(get_pay_dao)):
    new_payment = await dao.create(data)

    return "Payment created successfully"


@router.patch("/update/{id}", response_model=str)
async def update_payment(
    id: int, data: PaymentUpdate, dao: PaymentDao = Depends(get_pay_dao)
):
    updated_payment = await dao.update(id, data)
    if not updated_payment:
        raise ItemNotFound(item="payment", item_id=id)

    return "Payment updated successfully"


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(id: int, dao: PaymentDao = Depends(get_pay_dao)):
    await dao.delete(id)
    return "Payment deleted successfully"
