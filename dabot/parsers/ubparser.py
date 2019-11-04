

KEYS = ["BOOBS", "СИСКЕ"]
class UBParser(object):
    def __init__(self, msg_text):
        split_words = msg_text.split(' ')
        self.first_letters = [letters[0].upper() for letters in split_words]
        self.anagram = "".join(self.first_letters)
        self.msg = msg_text

    def valid(self):
        for key in KEYS:
            if key in self.anagram:
                return True
        return False

