import time
import uuid
from datetime import datetime, timedelta

import jwt
import requests
from jose import constants, jwe

from hbl_card_payment.utils import get_private_key, get_public_key, pad_amount


class HBLCardPayment:

    def __init__(
        self,
        merchant_id: str,
        api_key: str,
        encryption_key: str,
        callback_url: str,
        merchant_signing_private_key: str,
        paco_encryption_public_key: str,
        merchant_decryption_private_key: str,
        paco_signing_public_key: str,
    ) -> None:
        self.merchant_id = merchant_id
        self.api_key = api_key
        self.encryption_key = encryption_key
        self.merchant_signing_private_key = merchant_signing_private_key
        self.paco_encryption_public_key = paco_encryption_public_key
        self.merchant_decryption_private_key = merchant_decryption_private_key
        self.paco_signing_public_key = paco_signing_public_key
        self.request_payload = {
            "officeId": merchant_id,
            "paymentType": "CC",
            "paymentCategory": "ECOM",
            "storeCardDetails": {
                "storeCardFlag": "N",
                "storedCardUniqueID": "{{guid}}",
            },
            "installmentPaymentDetails": {
                "ippFlag": "N",
                "installmentPeriod": 0,
                "interestType": None,
            },
            "mcpFlag": "N",
            "request3dsFlag": "Y",
            "notificationURLs": {
                "confirmationURL": callback_url + "?payment=success",
                "failedURL": callback_url + "?payment=failed",
                "cancellationURL": callback_url + "?payment=cancel",
                "backendURL": callback_url + "?payment=backend",
            },
            "purchaseItems": [],
            "customFieldList": [],
        }

    def set_value(self, key, value):
        self.request_payload[key] = value

    def request(self, order_no: str, product_desc: str, amount: float):
        """prePaymentUI Payment Request"""

        now = datetime.now()

        self.request_payload["apiRequest"] = {
            "requestMessageID": str(uuid.uuid4()),
            "requestDateTime": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "language": "en-US",
        }
        self.request_payload["orderNo"] = order_no
        self.request_payload["productDescription"] = product_desc
        self.request_payload["transactionAmount"] = {
            "amountText": str(pad_amount(amount)),
            "currencyCode": "NPR",
            "decimalPlaces": 2,
            "amount": str(amount),
        }

        payload = {
            "request": self.request_payload,
            "iss": self.api_key,
            "aud": "PacoAudience",
            "CompanyApiKey": self.api_key,
            "iat": int(time.mktime(now.timetuple())),
            "nbf": int(time.mktime(now.timetuple())),
            "exp": int(time.mktime((now + timedelta(hours=1)).timetuple())),
        }

        signing_key = get_private_key(self.merchant_signing_private_key)
        encrypting_key = get_public_key(self.paco_encryption_public_key)

        body = self._encrypt_payload(payload, signing_key, encrypting_key)

        url = "https://core.paco.2c2p.com/api/1.0/Payment/prePaymentUi"
        headers = {
            "Accept": "application/jose",
            "CompanyApiKey": self.api_key,
            "Content-Type": "application/jose; charset=utf-8",
        }

        response = requests.post(url, headers=headers, data=body, timeout=100)

        if response.status_code != 200:
            response.raise_for_status()
        token = response.text

        decrypting_key = get_private_key(self.merchant_decryption_private_key)
        signature_verification_key = get_public_key(self.paco_signing_public_key)

        return self._decrypt_token(
            token=token,
            decrypt_key=decrypting_key,
            signature_verification_key=signature_verification_key,
        )

    def _decrypt_token(
        self, token: str, decrypt_key: str, signature_verification_key: str
    ):

        decrypted_token = jwe.decrypt(token, decrypt_key)

        decoded_token = jwt.decode(
            decrypted_token,
            key=signature_verification_key,
            algorithms="PS256",
            audience=self.api_key,
            issuer="PacoIssuer",
        )
        return decoded_token

    def _encrypt_payload(
        self, payload: str, signing_key: dict, encrypting_key: dict
    ) -> str:
        # Create JWS
        jws_token = jwt.encode(
            payload,
            signing_key,
            algorithm="PS256",
            headers={"typ": "JWT"},
        )

        # Create JWE
        jwe_header = {
            "algorithm": constants.ALGORITHMS.RSA_OAEP,
            "encryption": constants.ALGORITHMS.A128CBC_HS256,
            "kid": self.encryption_key,
            "cty": "JWT",
        }

        jwe_token = jwe.encrypt(jws_token, encrypting_key, **jwe_header)

        return jwe_token
