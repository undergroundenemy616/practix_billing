from uuid import UUID

from pydantic import BaseModel, condecimal, Field


class Payer(BaseModel):
    """ Class that can be used in payment by cryptogram."""
    first_name: str | None = Field(..., alias='FirstName')
    last_name: str | None = Field(..., alias='LastName')
    middle_name: str | None = Field(..., alias='MiddleName')
    birth: str | None = Field(..., alias='Birth')
    street: str | None = Field(..., alias='Street')
    address: str | None = Field(..., alias='Address')
    city: str | None = Field(..., alias='City')
    country: str | None = Field(..., alias='Country')
    phone: str | None = Field(..., alias='Phone')
    postcode: str | None = Field(..., alias='Postcode')


class CreatePaymentBase(BaseModel):
    """ Base class for other payment classes. """
    amount: condecimal(decimal_places=2) = Field(..., alias='Amount')
    currency: str | None = Field(..., alias='Currency')
    invoice_id: str | None = Field(..., alias='InvoiceId')
    description: str | None = Field(..., alias='Description')
    email: str | None = Field(..., alias='Email')


class CreatePaymentByCryptogram(CreatePaymentBase):
    """ Model for creating payment by card cryptogram (first time pay)."""
    ip_address: str = Field(..., alias='IpAddress')
    card_cryptogram_packet: str = Field(..., alias='CardCryptogramPacket')
    name: str | None = Field(..., alias='Name')
    payment_url: str | None = Field(..., alias='PaymentUrl')
    culture_name: str | None = Field(..., alias='CultureName')
    account_id: str | None = Field(..., alias='AccountId')
    payer: Payer | None = Field(..., alias='Payer')


class CreatePaymentByToken(CreatePaymentBase):
    """ Mode for creating payment with payment token (recurring payments)."""
    account_id: str = Field(..., alias='AccountId')
    token: str = Field(..., alias='Token')
    ip_address: str | None = Field(..., alias='IpAddress')
