import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from config import ENCRYPT_KEY, ENCRYPT_IV


def aes_encrypt(data: str) -> str:
    data = data.encode("utf-8")
    cipher = AES.new(ENCRYPT_KEY, AES.MODE_CBC, ENCRYPT_IV)
    data = cipher.encrypt(pad(data, 16, "pkcs7"))
    return base64.b64encode(data).decode("utf-8")


def aes_decrypt(data: str) -> str:
    data = base64.b64decode(data)
    cipher = AES.new(ENCRYPT_KEY, AES.MODE_CBC, ENCRYPT_IV)
    data = unpad(cipher.decrypt(data), 16, "pkcs7")
    return data.decode("utf-8")

