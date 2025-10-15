from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .product_schema import ProductRead, ProductWrite
from sqlalchemy import select, update, delete
from app.src.product.product_model import Product
from app.utils.custom_exceptions import ItemNotFound


class ProductDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> ProductRead | None:
        result = await self.db.execute(select(Product).where(Product.id == id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ProductRead] | None:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def create(self, data: ProductWrite) -> Product:
        new_product = Product(**data.model_dump())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Product).where(Product.id == id))
        product = result.scalar_one_or_none()
        if not product:
            raise ItemNotFound(item_id=id, item="product")

        await self.db.delete(product)
        await self.db.commit()
        return True


async def get_prod_dao(db: AsyncSession = Depends(get_db)) -> ProductDao:
    return ProductDao(db)
