import time
import hashlib
import hmac
import json
import requests


class MayfPayApi:

    def __init__(self, api_token: str, kassa_id: int, public_key: str, secret_key: str):
        self.api_token = api_token
        self.kassa_id = kassa_id
        self.public_key = public_key
        self.secret_key = secret_key
        self.base_url = "https://mayfpay.top/api/v2"

    def get_kassa_balance(self):
        url = f"{self.base_url}/kassa/balance"
        payload = {
            "api_token": self.api_token,
            "kassa_id": self.kassa_id,
        }
        headers = self._generate_auth_headers(payload)  # Pass payload as an argument
        response = requests.get(url, headers=headers, json=payload)
        response_json = response.json()
        return response_json

    def create_invoice(self, amount: float, order_id: str, expire_invoice: int, payment_method: str, comment: str, data: dict, en: bool = False, SubPayMethodId: str = None, successUrl: str = None, failUrl: str = None):
        url = f"{self.base_url}/kassa/invoice/create"
        payload = {
            "api_token": self.api_token,
            "kassa_id": self.kassa_id,
            "amount": amount,
            "order_id": order_id,
            "expire_invoice": expire_invoice,
            "en": en,
            "PayMethodId": payment_method,
            "SubPayMethodId": SubPayMethodId,
            "comment": comment,
            "successUrl": successUrl,
            "failUrl": failUrl,
            "data": data
        }

        headers = self._generate_auth_headers(payload) 
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        return response_json
    
    def check_invoice(self, order_id):
        url = f"{self.base_url}/kassa/invoice/check"
        payload = {
            "order_id": order_id,
            "api_token": self.api_token,
            }
        headers = self._generate_auth_headers(payload)
        response = requests.get(url, headers=headers, json=payload)
        return response.json()
    
    def _generate_auth_headers(self, payload=None):
        timestamp = str(time.time())
        headers = {
            "timestamp": timestamp,
            "x-api-public-key": self.public_key,
            "x-api-signature": self._generate_signature(payload),
            "Content-Type": "application/json"
        }
        return headers
    
    def _generate_signature(self, payload):
        payload_str = json.dumps(payload)
        signature = hmac.new(self.secret_key.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        return signature
    


