from fastapi import APIRouter, Depends

from models.payments import CreatePaymentByCryptogram, PaymentResult, \
    CreatePaymentByToken, CreatePaymentBy3DS
from services.payments import PaymentsService, get_payments_service

router = APIRouter()


@router.post('/cards/charge',
             response_model=PaymentResult, response_model_by_alias=True,
             response_model_exclude_unset=True)
async def cards_charge(
        payment: CreatePaymentByCryptogram,
        payments_service: PaymentsService = Depends(get_payments_service)
):
    return await payments_service.cards_charge()


@router.post('/tokens/charge',
             response_model=PaymentResult, response_model_by_alias=True,
             response_model_exclude_unset=True)
async def tokens_charge(
        payment: CreatePaymentByToken,
        payments_service: PaymentsService = Depends(get_payments_service)
):
    return await payments_service.tokens_charge()


@router.post('/cards/post3ds',
             response_model=PaymentResult, response_model_by_alias=True,
             response_model_exclude_unset=True)
async def post_3ds(
        payment: CreatePaymentBy3DS,
        payments_service: PaymentsService = Depends(get_payments_service)
):
    return await payments_service.post3ds()
