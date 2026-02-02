from enum import IntEnum


class ProductStatus(IntEnum):
    ACTIVE = 0
    ARCHIVED = 1


class OrderStatus(IntEnum):
    PROCESSING = 0
    ONHOLD = 1
    COMPLETED = 2
    REJECTED = 3
