from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.enums import ProductStatus
from .schema import ProductRead, ProductWrite, ProductBase
from sqlalchemy import select
from app.src.product.model import Product
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound


class ProductDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> ProductRead | None:
        result = await self.db.execute(
            select(Product)
            .options(selectinload(Product.base_expenses))
            .where(Product.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ProductRead] | None:
        result = await self.db.execute(
            select(Product).options(selectinload(Product.base_expenses))
        )
        return result.scalars().all()

    async def get_all_archived(self) -> list[ProductRead] | None:
        result = await self.db.execute(
            select(Product)
            .options(selectinload(Product.base_expenses))
            .where(Product.is_archived == ProductStatus.ARCHIVED.value)
        )
        return result.scalars().all()

    async def get_all_active(self) -> list[ProductRead] | None:
        result = await self.db.execute(
            select(Product)
            .options(selectinload(Product.base_expenses))
            .where(Product.is_archived == ProductStatus.ACTIVE.value)
        )
        return result.scalars().all()

    async def put_to_archive(self, id: int) -> bool:
        result = await self.db.get(Product, id)
        if not result:
            raise ItemNotFound(item_id=id, item="product")
        result.is_archived = ProductStatus.ARCHIVED.value
        await self.db.commit()
        await self.db.refresh(result)
        return True

    async def delete_from_archive(self, id: int) -> bool:
        result = await self.db.get(Product, id)
        if not result:
            raise ItemNotFound(item_id=id, item="product")
        result.is_archived = ProductStatus.ACTIVE.value
        await self.db.commit()
        await self.db.refresh(result)
        return True

    async def create(self, data: ProductWrite) -> Product:
        new_product = Product(**data.model_dump())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def update(self, id: int, data: ProductBase) -> Product:
        result = await self.db.get_one(Product, id)
        if not result:
            raise ItemNotFound(item_id=id, item="order")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result

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
