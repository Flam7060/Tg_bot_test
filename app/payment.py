import uuid
import yookassa
from yookassa import Payment

from config import Y_KASSA

# yookassa.Configuration.account_id = '506751'
# yookassa.Configuration.secret_key = Y_KASSA

# def create(amount, chat_id):
#     id_key = str(uuid.uuid4())
#     payment = Payment.create({
#         "amount": {
#             "value": amount,
#             "currency": "RUB"
#         },
#         "confirmation": {
#             "type": "redirect",
#             "return_url": "https://t.me/styug_bot"
#         },
#         "capture": True,
#         'metadata': {
#             'chat_id': chat_id
#         },
#         "description": "Заказ №1"
#     },id_key)
#     return payment.confirmation.confirmation_url, id_key
