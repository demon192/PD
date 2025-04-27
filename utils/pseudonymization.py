import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import pandas as pd


def apply_pseudoanonymization(value, technique):
    if pd.isnull(value):
        return value
    value = str(value)

    if technique == "AES-SIV":
        key = AESGCM.generate_key(bit_length=128)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, value.encode(), None)
        return base64.b64encode(nonce + ct).decode()

    elif technique == "HMAC-MD5":
        return hashlib.md5(value.encode()).hexdigest()

    elif technique == "SHA256":
        return hashlib.sha256(value.encode()).hexdigest()

    elif technique == "Random String":
        return base64.b64encode(os.urandom(6)).decode()

    else:
        return value
