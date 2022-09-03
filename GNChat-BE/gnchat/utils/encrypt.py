import json

from gnchat.utils.formatter import data_formatter


def decrypt(data):
    data = json.loads(data.decode('utf-8')).get('data')
    res = bytearray()
    res.extend(byte - 1 for byte in data)
    return json.loads(res.decode('utf-8'))


def encrypt(data):
    data = data_formatter(data)
    string = json.dumps(data)
    res = [byte + 1 for byte in bytearray(string, 'utf-8')]
    return res
