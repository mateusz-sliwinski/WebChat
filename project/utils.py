from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from dotenv import load_dotenv
import os


def get_password_data() -> [str, bytes]:
    load_dotenv()
    password = os.environ.get('PASSWORD')
    password_salt = bytes(os.environ.get('PASSWORD_SALT'), encoding='utf-8')

    return password, password_salt


def string_to_code(message: str) -> [bytes, bytes]:
    password, password_salt = get_password_data()

    key = PBKDF2(password, password_salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_message = cipher.encrypt(pad(bytes(message, encoding='utf-8'), AES.block_size))
    initialization_vector = cipher.iv

    return encrypted_message, initialization_vector


def code_to_string(encrypted_message: bytes, initialization_vector: bytes) -> str:
    password, password_salt = get_password_data()

    key = PBKDF2(password, password_salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv=initialization_vector)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)

    return str(decrypted_message)
