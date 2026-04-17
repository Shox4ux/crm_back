from enum import IntEnum


class ProductStatus(IntEnum):
    ACTIVE = 0
    ARCHIVED = 1


class OrderStatus(IntEnum):
    PAID = 0
    PREPAID = 1
    UNPAID = 2
    RETURN = 3
    REFUND = 4


class CancelType(IntEnum):
    RETURN = 3
    REFUND = 4
