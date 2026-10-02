from enum import Enum

from pydantic import BaseModel, Field


class EmailCategory(str, Enum):
    SALES_LEAD = "SALES_LEAD"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    INVOICE = "INVOICE"
    QUOTATION = "QUOTATION"
    APPOINTMENT = "APPOINTMENT"
    APPLICATION = "APPLICATION"
    COMPLAINT = "COMPLAINT"
    GENERAL_ENQUIRY = "GENERAL_ENQUIRY"
    INTERNAL = "INTERNAL"
    SPAM = "SPAM"
    OTHER = "OTHER"


class EmailClassification(BaseModel):
    category: EmailCategory
    confidence: float = Field(ge=0.0, le=1.0)
    urgency: str
    intent: str
    reason: str