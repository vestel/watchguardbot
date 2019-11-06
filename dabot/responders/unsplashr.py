import telepot
import datetime

from parsers.unsplashp import UnsplashParser
from settings import INDEX_START

class UnsplashResponder(object):
    def __init__(self, msg, unsplash):
        msg_type, _chat_type, chat_id = telepot.glance(msg)
        self.valid =  msg_type == 'text'
        if self.valid:
            parser = UnsplashParser(msg['text'])
            self.valid = parser.valid()
        self.index = int(msg['message_id'])-INDEX_START
        if not self.valid and (self.index % 42 == 0):
            self.valid = 'fox'
        if not (datetime.time(hour=6, minute=0) < datetime.datetime.now().time() < datetime.time(hour=22, minute=0)):
            self.valid = False
        self.reply_to = msg['message_id']
        self.api = unsplash

    def response_url(self):
        key = self.valid
        lst = self.api.photos(type_='random', count=1, query=key)
        for one in lst.entries:
            url = one.link_download
            self.image = one.body
        return url

    def response_params(self):
        return {'disable_notification': True,
                'reply_to_message_id': self.reply_to,
                'parse_mode': 'Markdown',
                'caption': """Чуйка подсказывает, что вы ждете эту картинку. 
Photo by [{}]({}) on [Unsplash]({})""".format(self.image['user']['name'],
            self.image['user']['links']['html'],
            "https://unsplash.com/?utm_source=DarwinMoodBot&utm_medium=referral")}
