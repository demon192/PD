import pandas as pd
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import random
import string

counter_store = {}

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
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(10))

    elif technique == "Encrypted Counter":
        if value not in counter_store:
            counter_store[value] = len(counter_store) + 1
        return f"ENC-{counter_store[value]}"

    elif technique == "SHA2-256":
        return hashlib.sha256(value.encode()).hexdigest()

    elif technique == "Simple Counter":
        if value not in counter_store:
            counter_store[value] = len(counter_store) + 1
        return counter_store[value]

    elif technique == "AES Encryption":
        key = AESGCM.generate_key(bit_length=128)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, value.encode(), None)
        return base64.b64encode(nonce + ct).decode()

    elif technique == "Encrypted Hash":
        hash_value = hashlib.sha256(value.encode()).hexdigest()
        key = AESGCM.generate_key(bit_length=128)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, hash_value.encode(), None)
        return base64.b64encode(nonce + ct).decode()

    else:
        return value
