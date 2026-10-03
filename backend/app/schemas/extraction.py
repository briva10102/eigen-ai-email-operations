from typing import Optional

from pydantic import BaseModel, Field


class SalesLeadExtraction(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    product_interest: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    requirements: Optional[str] = None
    urgency: Optional[str] = None


class InvoiceExtraction(BaseModel):
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    tax: Optional[float] = None