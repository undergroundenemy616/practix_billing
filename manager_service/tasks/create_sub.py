import uuid

from celery import shared_task
from subscribtions.models import Tariff


@shared_task
def create_sub(id_: uuid.UUID, tariff: Tariff, cryptogram: str):
    pass
