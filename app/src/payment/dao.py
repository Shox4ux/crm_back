from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import PaymentCreate, PaymentResponse, PaymentUpdate
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload
from app.src.client.model import Client
from app.utils.custom_exceptions import ItemNotFound
from .model import Payment


class PaymentDao:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db: AsyncSession = db

    async def get_all(self) -> list[PaymentResponse] | None:
        result = await self.db.execute(
            select(Payment).options(
                selectinload(Payment.client).selectinload(Client.user),
                selectinload(Payment.order),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, id: int) -> PaymentResponse:
        result = await self.db.execute(select(Payment).where(Payment.id == id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise ItemNotFound(item="payment", item_id=id)
        return payment

    async def create(self, data: PaymentCreate) -> PaymentResponse:
        stmt = insert(Payment).values(**data.model_dump()).returning(Payment)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def update(self, id: int, data: PaymentUpdate) -> bool:
        stmt = (
            update(Payment)
            .where(Payment.id == id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(Payment)
        )
        up_payment = await self.db.execute(stmt)

        if not up_payment:
            raise ItemNotFound(item="payment", item_id=id)

        await self.db.commit()
        return True

    async def delete(self, id: int) -> None:
        stmt = delete(Payment).where(Payment.id == id).returning(Payment.id)
        result = await self.db.execute(stmt)
        deleted_id = result.scalar_one_or_none()
        if deleted_id is None:
            raise ItemNotFound(item="payment", item_id=id)
        await self.db.commit()


async def get_pay_dao(db: AsyncSession = Depends(get_db)) -> PaymentDao:
    return PaymentDao(db=db)
