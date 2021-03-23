# -*- coding: utf-8 -*-

import os
import json
import base64
import sqlite3
import binascii
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def get_string(file):
    with open(file, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s


def pull_the_key(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    key_header = encrypted_key_with_header[5:]
    decode_key = win32crypt.CryptUnprotectData(key_header, None, None, None, 0)[1]
    return decode_key


def decrypt_string(decode_key, data):
    nonce, cipher_bytes = data[3:15], data[15:]
    plain_text = AESGCM(decode_key).decrypt(nonce, cipher_bytes, None).decode('utf-8')
    return plain_text

sql = "select host_key,name,encrypted_value from cookies"
# sql = "SELECT action_url, username_value, password_value FROM logins"

# cookie key
local_state = r'D:\code\Local State'
encrypted_key = get_string(local_state)
key = pull_the_key(encrypted_key)
print(encrypted_key)
print(key)

cookie_file = "D:\\code\\Cookies"
password_file = "D:\\code\\Login Data"

with sqlite3.connect(cookie_file) as conn:
    cursor = conn.cursor()
    result_list = cursor.execute(sql).fetchall()
    cursor.close()
    for result in result_list:
        if not result[0]:
            continue

        try:
            if result[2][0:3] == b'v10':
                password = decrypt_string(key, result[2])
            else:
                password = win32crypt.CryptUnprotectData(result[2])[1].decode()
        except Exception as e:
            password = result[2]
            print("Domain: %s; User: %s; Exception: %s; Password: %s" % (result[0], result[1], e, result[2]))

        print("Domain: %s; User: %s; Password: %s" % (result[0], result[1], password))
