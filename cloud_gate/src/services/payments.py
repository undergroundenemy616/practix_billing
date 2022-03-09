from functools import lru_cache

from faker import Faker

from models.payments import PaymentResult, PaymentResultModel

fake = Faker()


class PaymentsService:
    async def cards_charge(self) -> PaymentResult:
        return PaymentResult(
            success=True,
            message=None,
            model=PaymentResultModel(
                transaction_id=fake.pyint(),
                token=fake.uuid4(),
                reason_code=0,
            ),
        )

    async def tokens_charge(self) -> PaymentResult:
        return await self.cards_charge()

    async def post3ds(self) -> PaymentResult:
        # Review Comment: ввиду инкапсуляции зависимостей приянтно решение
        # использовать ООП подход. Три метода реализуют различные эндпоинты
        # платежного API: оплата по криптограмме, по токену и с 3D Secure.
        # Сейчас вывод одинаков, но при тестировании может быть добавлена
        # иная логика в эмулятор на разные эндпоинты.
        return await self.cards_charge()


@lru_cache()
def get_payments_service() -> PaymentsService:
    return PaymentsService()
