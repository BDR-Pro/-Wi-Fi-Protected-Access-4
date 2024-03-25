from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import hashlib

import string
import random

 

def generate_key():
    eth_k = generate_eth_key()
    sk_hex = eth_k.to_hex()  # hex string
    pk_hex = eth_k.public_key.to_hex()  # hex string
    return sk_hex, pk_hex


def encrypt_message(pk_hex, data):
    return encrypt(pk_hex, data)

def decrypt_message(sk_hex, ciphertext):
    return decrypt(sk_hex, ciphertext)


def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def generate_random_salt():
    # using random.choices()
    # generating random strings
    return ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=50))