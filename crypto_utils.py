import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

NONCE_SIZE = 12
TAG_SIZE = 16
KEY_SIZE = 32

def ensure_key_from_base64(b64_key: str) -> bytes:
    key = base64.b64decode(b64_key)
    if len(key) != KEY_SIZE:
        raise ValueError("MASTER_KEY must decode to 32 bytes")
    return key

def encrypt_bytes(plaintext: bytes, key: bytes) -> dict:
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return {"ciphertext": ciphertext, "nonce": nonce, "tag": tag}

def decrypt_bytes(ciphertext: bytes, nonce: bytes, tag: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def pack_to_store(ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
    return nonce + tag + ciphertext

def unpack_from_store(stored: bytes) -> tuple:
    nonce = stored[:NONCE_SIZE]
    tag = stored[NONCE_SIZE:NONCE_SIZE+TAG_SIZE]
    ciphertext = stored[NONCE_SIZE+TAG_SIZE:]
    return ciphertext, nonce, tag
