KEYS = {"ЕЖИК": 'hedgehog', "ЛИСА": 'fox', "ПСИНА": 'dog', "КСЮША": 'horse', "РЫБА": 'fish', "СВИН": 'pig'}
class UnsplashParser(object):
    def __init__(self, msg_text):
        split_words = msg_text.split(' ')
        self.first_letters = [letters[0].upper() if len(letters)>1 else "" for letters in split_words]
        self.abbr = "".join(self.first_letters)
        self.msg = msg_text

    def valid(self):
        for key in list(KEYS.keys()):
            if key in self.abbr:
                return KEYS[key]
        return False
