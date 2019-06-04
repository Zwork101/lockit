from os import remove

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor


def wrap(string: bytes, max: int = 32):
    split_string = [string[i:i + max] for i in range(0, len(string), max)]
    start_string = split_string.pop(0)
    for string in split_string:
        start_string = strxor(start_string, string)
    return start_string


def sterilize(password: str):
    password = password.encode()
    if len(password) > 32:
        password = wrap(password)
    for i in (16, 24, 32):
        if len(password) < i:
            password = pad(password, i)
            break
    return password


class EncryptedFile:

    def __init__(self, name, password: str):
        self.name = name + ".lck" if not name.endswith(".lck") else name
        self.password = sterilize(password)
        self.cipher = AES.new(self.password, AES.MODE_ECB)

    def transfer_file(self, file_path: str):
        with open(file_path, "rb") as original_file:
            with open(self.name, "wb") as new_file:
                data = pad(original_file.read(), AES.block_size)
                data = self.cipher.encrypt(data)
                new_file.write(data)
        remove(file_path)

    def unpack_file(self):
        with open(self.name, "rb") as original_file:
            with open(self.name[:-4], "wb") as new_file:
                data = self.cipher.decrypt(original_file.read())
                data = unpad(data, AES.block_size)
                new_file.write(data)
        remove(self.name)
        return self.name[:-4]
