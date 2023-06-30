from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from dotenv import load_dotenv
import os


def string_to_code(message: str):
    load_dotenv()
    PASSWORD = os.environ.get('PASSWORD')
    PASSWORD_SALT = bytes(os.environ.get('PASSWORD_SALT'), encoding='utf-8')
    key = PBKDF2(PASSWORD, PASSWORD_SALT, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)
    cipher_data = cipher.encrypt(pad(bytes(message, encoding='utf-8'), AES.block_size))

    return cipher_data, cipher.iv



