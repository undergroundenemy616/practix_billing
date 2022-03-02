import os
from uuid import UUID

import httpx
from celery import shared_task
from httpx import Response

from subscribtions.models import Bill, Payment


class PaymentProcessor:
    """ Class to process bill payments via payment gate"""

    def __init__(self, bill: Bill):
        self.bill = bill
        self.payment_id = None
        self.gate_uri = os.environ.get('GATE_URI')

    def pay(self) -> UUID:
        if self.bill.status == Bill.BillStatuses.NOT_PAID:
            return

        match self.bill.payment_type:
            case Bill.PaymentType.CRYPTOGRAM:
                self._pay_with_cryptogram()
            case Bill.PaymentType.TOKEN:
                self._pay_with_token()
            case Bill.PaymentType.POST3DS:
                self._pay_with_3ds()
            case _:
                pass
        return self.payment_id

    @staticmethod
    def _is_payment_successful(response: Response):
        if response.status_code != httpx.codes.OK:
            return False
        if response.headers.get('content-type') != 'application/json':
            return False
        if response.json()['Success']:
            return True
        return False

    def _save_token_and_transaction(self, response: Response):
        """ Save successful transaction id and token."""
        transaction_id = response.json()['Model']['TransactionId']
        token = response.json()['Model']['Token']
        payment = Payment(bill=self.bill,
                          transaction_id=transaction_id,
                          is_success=True)
        payment.save()
        self.payment_id = payment.id

        self.bill.status = Bill.BillStatuses.PAID
        self.bill.save()

        account = self.bill.account
        account.token = token
        account.save()

    def _save_fault_transaction(self):
        payment = Payment(bill=self.bill, is_success=False)
        payment.save()
        self.payment_id = payment.id

    def _pay_with_cryptogram(self):
        amount: int = self.bill.amount
        ip_address: str = self.bill.ip_address
        card_cryptogram_packet: str = self.bill.card_cryptogram_packet
        payload = {'amount': amount,
                   'ip_address': ip_address,
                   'card_cryptogram_packet': card_cryptogram_packet
                   }
        url = f'{self.gate_uri}/cards/charge'
        response = httpx.post(url, json=payload)

        if self._is_payment_successful(response):
            self._save_token_and_transaction(response)
        else:
            self._save_fault_transaction()

    def _pay_with_token(self):
        amount: int = self.bill.amount
        account_id: str = self.bill.account.id
        token: str = self.bill.account.payment_token
        payload = {'amount': amount,
                   'account_id': account_id,
                   'token': token
                   }
        url = f'{self.gate_uri}/tokens/charge'
        response = httpx.post(url, json=payload)

        if self._is_payment_successful(response):
            self._save_token_and_transaction(response)
        else:
            self._save_fault_transaction()

    def _pay_with_3ds(self):
        transaction_id: int = self.bill.transaction_id
        pa_res: str = self.bill.pa_res
        payload = {'transaction_id': transaction_id,
                   'pa_res': pa_res
                   }
        url = f'{self.gate_uri}/cards/post3ds'
        response = httpx.post(url, json=payload)

        if self._is_payment_successful(response):
            self._save_token_and_transaction(response)
        else:
            self._save_fault_transaction()


@shared_task
def make_payment_on_bill(bill_uuid: UUID):
    bill = Bill.objects.get(id=bill_uuid)
    if bill:
        processor = PaymentProcessor(bill)
        processor.pay()
