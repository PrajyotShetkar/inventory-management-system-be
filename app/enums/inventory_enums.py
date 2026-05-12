import enum


class IndustryType(str, enum.Enum):
    RETAIL = "Retail"
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    FOOD_AND_BEVERAGE = "Food & Beverage"
    HARDWARE = "Hardware"
    GENERAL_MERCHANDISE = "General Merchandise"


class PaymentTerms(str, enum.Enum):
    NET_15 = "Net 15"
    NET_30 = "Net 30"
    NET_45 = "Net 45"
    NET_60 = "Net 60"
    COD = "Cash on Delivery"


class ItemCategory(str, enum.Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food"
    FURNITURE = "Furniture"
    STATIONERY = "Stationery"
    TOOLS = "Tools"
    OTHER = "Other"


class POStatus(str, enum.Enum):
    DRAFT = "Draft"
    CONFIRMED = "Confirmed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class SaleStatus(str, enum.Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"
    REFUNDED = "Refunded"


class PaymentMethod(str, enum.Enum):
    CASH = "Cash"
    CARD = "Card"
    BANK_TRANSFER = "Bank Transfer"
    ONLINE = "Online"


class ChangeType(str, enum.Enum):
    PURCHASE_RECEIPT = "Purchase Receipt"
    SALE = "Sale"
    MANUAL_ADJUSTMENT = "Manual Adjustment"
    RETURN = "Return"
    REORDER_ALERT = "Reorder Alert"
    OTHER = "Other"
