KEYS = {"ЕЖИК": 'hedgehog', "ЛИСА": 'fox', "ПСИНА": 'dog', "КСЮША": 'horse', "ФИШКА": 'fish', "ЛЕВА": 'lion',
        "СВИН": 'pig', "МУРКА": 'kitty', "БАРСИК": 'cat', "КАРКАР": 'bird', "ТИГРА": 'tiger', "КЕША": 'parrot',
        "ТАИГА": 'wildlife', "ПЛЯЖ": 'beach', "ЛУЖА": 'ocean', "ОХОТА": 'safari', "МИША": 'bear', "КУНФУ": 'panda',
        "ЛОЛО": 'penguin', "МЕЛМАН": 'giraffe', "РАКЕТА": 'racoon', "МАРТИ": "zebra", "ГЛОРИЯ": 'hippo',
        "ГОРА": 'mountain', "НЕБО": 'sky', "ОБЛАКО": 'cloud', "УТЕС": 'cliff', "ОТПУСК": 'vacation',
        "ЧУВИХА": 'beautiful-girl', "ЧУВАК": 'male-model', "ШТИК": 'love', "ЖАРА": 'sexy', "СОПЛИ": 'romance'}

class UnsplashParser(object):
    def __init__(self, msg_text):
        split_words = msg_text.split(' ')
        self.first_letters = [letters[0].upper() if len(letters)>1 else "" for letters in split_words]
        self.abbr = "".join(self.first_letters)
        self.msg = msg_text

    def valid(self):
        for key in list(KEYS.keys()):
            if key in self.abbr:
                print('Keyword: {} '.format(KEYS[key]), end='')
                return KEYS[key]
        return False
