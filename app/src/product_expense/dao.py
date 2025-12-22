from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import ProdExpRead, ProdExpWrite, ProdExpBulkWrite
from sqlalchemy import select
from app.src.product_expense.model import ProductExpense
from app.utils.custom_exceptions import ItemNotFound
from typing import Optional


class ProdExpDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> ProdExpRead | None:
        result = await self.db.execute(
            select(ProductExpense).where(ProductExpense.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ProdExpRead] | None:
        result = await self.db.execute(select(ProductExpense))
        return result.scalars().all()

    async def create(self, data: ProdExpBulkWrite) -> Optional[list[ProdExpRead]]:
        prods = [
            ProductExpense(
                product_id=data.product_id, name=item.name, amount=item.amount
            )
            for item in data.items
        ]

        self.db.add_all(prods)
        await self.db.commit()
        return prods

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(
            select(ProductExpense).where(ProductExpense.id == id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise ItemNotFound(item_id=id, item="product_expense")

        await self.db.delete(product)
        await self.db.commit()
        return True

    async def update(self, id: int, data: ProdExpWrite) -> ProductExpense:
        result = await self.db.get_one(ProductExpense, id)

        if not result:
            raise ItemNotFound(item_id=id, item="product_expense")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result


async def get_prod_exp_dao(db: AsyncSession = Depends(get_db)) -> ProdExpDao:
    return ProdExpDao(db)
