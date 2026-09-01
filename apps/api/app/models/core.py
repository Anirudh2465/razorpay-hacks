import enum
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, DateTime, Numeric, Enum, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    legal_name: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    phone: Mapped[Optional[str]] = mapped_column(String)
    tax_id: Mapped[Optional[str]] = mapped_column(String)
    country: Mapped[str] = mapped_column(String, default="IN")
    status: Mapped[CustomerStatus] = mapped_column(Enum(CustomerStatus), default=CustomerStatus.ACTIVE)

    invoices = relationship("Invoice", back_populates="customer")

class InvoiceStatus(str, enum.Enum):
    ISSUED = "issued"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    invoice_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    customer_ref_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer_name: Mapped[str] = mapped_column(String)
    invoice_date: Mapped[date] = mapped_column(Date)
    due_date: Mapped[date] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String, default="INR")
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    discount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus), default=InvoiceStatus.ISSUED)
    purchase_order_id: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    customer = relationship("Customer", back_populates="invoices")

class PaymentStatus(str, enum.Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PENDING = "pending"
    REVERSED = "reversed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"

class PaymentMethod(str, enum.Enum):
    UPI = "UPI"
    CARD = "card"
    NETBANKING = "netbanking"
    BANK_TRANSFER = "bank_transfer"
    WALLET = "wallet"

class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    payment_id: Mapped[str] = mapped_column(String, unique=True, index=True) # Razorpay pay_id
    invoice_reference: Mapped[Optional[str]] = mapped_column(String) # From payer
    customer_id: Mapped[Optional[str]] = mapped_column(String)
    customer_name: Mapped[str] = mapped_column(String)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String, default="INR")
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod))
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus))
    transaction_reference: Mapped[Optional[str]] = mapped_column(String)
    gateway_reference: Mapped[Optional[str]] = mapped_column(String)
    route_rule_id: Mapped[Optional[str]] = mapped_column(String)

class RouteTransfer(Base, TimestampMixin):
    __tablename__ = "route_transfers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transfer_id: Mapped[str] = mapped_column(String, unique=True, index=True) # trf_id
    payment_id: Mapped[str] = mapped_column(String, index=True)
    route_rule_id: Mapped[str] = mapped_column(String)
    linked_account_id: Mapped[str] = mapped_column(String)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    leg_type: Mapped[str] = mapped_column(String) # "vendor" or "platform"

class BankSettlement(Base, TimestampMixin):
    __tablename__ = "bank_settlements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    utr: Mapped[str] = mapped_column(String, unique=True, index=True)
    settlement_batch_id: Mapped[Optional[str]] = mapped_column(String)
    linked_account_id: Mapped[str] = mapped_column(String)
    amount_credited: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    value_date: Mapped[date] = mapped_column(Date)
    razorpay_transfer_id: Mapped[Optional[str]] = mapped_column(String)
    narration: Mapped[Optional[str]] = mapped_column(String)
