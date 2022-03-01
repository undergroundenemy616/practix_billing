import os

from subscribtions.models import Bill


class PaymentProcessor:
    """ Class to process bill payments via payment gate"""
    def __init__(self, bill: Bill):
        self.bill = bill
        self.gate_host = os.environ.get('GATE_HOST')
        self.gate_port = os.environ.get('GATE_PORT')

    def pay_with_cryptogram(self):
        pass

    def pay_with_token(self):
        pass

    def pay_with_3ds(self):
        pass