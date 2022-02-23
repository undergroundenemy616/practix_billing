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
    currency: str | None = Field(None, alias='Currency')
    invoice_id: str | None = Field(None, alias='InvoiceId')
    description: str | None = Field(None, alias='Description')
    email: str | None = Field(None, alias='Email')


class CreatePaymentByCryptogram(CreatePaymentBase):
    """ Model for creating payment by card cryptogram (first time pay)."""
    ip_address: str = Field(..., alias='IpAddress')
    card_cryptogram_packet: str = Field(..., alias='CardCryptogramPacket')
    name: str | None = Field(None, alias='Name')
    payment_url: str | None = Field(None, alias='PaymentUrl')
    culture_name: str | None = Field(None, alias='CultureName')
    account_id: str | None = Field(None, alias='AccountId')
    payer: Payer | None = Field(None, alias='Payer')


class CreatePaymentByToken(CreatePaymentBase):
    """ Model for creating payment with payment token (recurring payments)."""
    account_id: str = Field(..., alias='AccountId')
    token: str = Field(..., alias='Token')
    ip_address: str | None = Field(None, alias='IpAddress')


class CreatePaymentBy3DS(BaseModel):
    """ Model for creating payment via 3DS verification on the front-end. """
    transaction_id: int = Field(..., alias='TransactionId')
    pa_res: str = Field(..., alias='PaRes')


class PaymentResultModel(BaseModel):
    """ Model represents additional data in transaction response."""
    reason_code: int | None = Field(None, alias='ReasonCode')
    token: str | None = Field(None, alias='Token')
    transaction_id: int = Field(..., alias='TransactionId')
    reason: str | None = Field(None, alias='Reason')
    card_holder_message: str | None = Field(None, alias='CardHolderMessage')

    class Config:
        allow_population_by_field_name = True


class PaymentResult(BaseModel):
    """ Model for response from gate after payment."""
    success: bool = Field(..., alias='Success')
    message: str | None = Field(None, alias='Message')
    model: PaymentResultModel | None = Field(None, alias='Model')

    class Config:
        allow_population_by_field_name = True
