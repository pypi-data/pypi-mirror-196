import hashlib
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt(message: str, key: str) -> bytes:
    message = message.encode('utf-8')
    key = key.encode('utf-8')
    salt = hashlib.sha256(str(random.randint(0, 1000000000)).encode()).hexdigest().encode()
    kdf = hashlib.pbkdf2_hmac('sha512', key, salt, 100000)
    key = kdf[:32]
    iv = bytearray(random.getrandbits(8) for i in range(16))
    padded_message = pad(message, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_message = cipher.encrypt(padded_message)
    return salt + iv + encrypted_message


def decrypt(encrypted_message: bytes, key: str) -> str:
    salt = encrypted_message[:64]
    iv = encrypted_message[64:80]
    encrypted_message = encrypted_message[80:]
    kdf = hashlib.pbkdf2_hmac('sha512', key.encode('utf-8'), salt, 100000)
    key = kdf[:32]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(encrypted_message)
    unpadded_message = unpad(decrypted_message, 16)
    return unpadded_message.decode('utf-8')