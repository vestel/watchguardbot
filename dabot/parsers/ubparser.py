# -*- coding: utf-8 -*-
import hashlib

KEYS = ["BOOBS", "СИСКЕ", "TITTY", "ГРУД", "СОСОК"]
SECRET_HASH = "ebb3018876b2006b4a2fb8162714807e7c3204c209a91a390dfa73d26ac60adb"

class UBParser(object):
    def __init__(self, msg_text):
        split_words = msg_text.split(' ')
        self.first_letters = [letters[0].upper() if len(letters)>1 else "" for letters in split_words]
        self.anagram = "".join(self.first_letters)
        self.msg = msg_text.replace("\r", "").replace("\n", "").strip()
        self.hash = hashlib.sha256()

    def valid(self):
        for key in KEYS:
            if key in self.anagram:
                return True
        self.hash.update(self.msg.encode('utf-8'))
        msg_hash = self.hash.hexdigest()
        val = bool(msg_hash.lower()==SECRET_HASH.lower())
        return val

