from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import PaymentCreate, PaymentResponse, PaymentUpdate
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound
from .model import Payment


class PaymentDao:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db: AsyncSession = db

    async def get_all(self) -> list[PaymentResponse] | None:
        result = await self.db.execute(select(Payment))
        return result.scalars().all()

    async def create(self, data: PaymentCreate) -> PaymentResponse:
        new_payment = data.to_payment()
        self.db.add(new_payment)
        await self.db.commit()
        await self.db.refresh(new_payment)
        return new_payment

    async def get_by_id(self, id: int) -> PaymentResponse:
        result = await self.db.execute(select(Payment).where(Payment.id == id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise ItemNotFound(item="payment", item_id=id)

        return payment

    async def update(self, id: int, data: PaymentUpdate) -> PaymentResponse:
        result = await self.db.execute(select(Payment).where(Payment.id == id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise ItemNotFound(item="payment", item_id=id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(payment, key, value)
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def delete(self, id: int) -> None:
        result = await self.db.execute(select(Payment).where(Payment.id == id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise ItemNotFound(item="payment", item_id=id)
        await self.db.delete(payment)
        await self.db.commit()


async def get_pay_dao(db: AsyncSession = Depends(get_db)) -> PaymentDao:
    return PaymentDao(db=db)
