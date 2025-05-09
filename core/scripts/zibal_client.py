import requests
import json

class ZibalSandbox:
    _payment_request_url = "https://sandbox.zibal.ir/v1/request"
    _payment_verify_url = "https://sandbox.zibal.ir/v1/verify"
    _payment_page_url = "https://sandbox.zibal.ir/start/"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, merchant_id):
        self.merchant_id = merchant_id

    def payment_request(self, amount, description="پرداختی کاربر"):
        payload = {
            "merchant": self.merchant_id,
            "amount": amount,
            "callbackUrl": self._callback_url,
            "description": description
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self._payment_request_url, headers=headers, data=json.dumps(payload))

        return response.json()

    def payment_verify(self, amount, track_id):
        payload = {
            "merchant": self.merchant_id,
            "amount": amount,
            "trackId": track_id
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, track_id):
        return self._payment_page_url + str(track_id)
