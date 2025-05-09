import requests
import json

class IDPaySandbox:
    _payment_request_url = "https://api.idpay.ir/v1.1/payment"
    _payment_verify_url = "https://api.idpay.ir/v1.1/payment/verify"
    _payment_page_url = "https://idpay.ir/p/ws/"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, api_key):
        self.api_key = api_key

    def payment_request(self, amount, order_id="123456", description="پرداختی کاربر"):
        payload = {
            "order_id": order_id,
            "amount": amount,
            "callback": self._callback_url,
            "description": description
        }
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_key,
            'X-SANDBOX': '1'
        }

        response = requests.post(
            self._payment_request_url, headers=headers, data=json.dumps(payload))

        return response.json()

    def payment_verify(self, id, order_id):
        payload = {
            "id": id,
            "order_id": order_id
        }
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_key,
            'X-SANDBOX': '1'
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, id):
        return self._payment_page_url + id
