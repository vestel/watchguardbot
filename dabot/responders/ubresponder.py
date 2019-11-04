import math
import re
import telepot
import urllib.request

from parsers.ubparser import UBParser
from settings import INDEX_START

URL = 'https://tits-guru.com/randomTits'
REGEXP = re.compile(r'contentUrl\" content=\"(.*)\"')
class UBResponder(object):
    def __init__(self, msg):
        msg_type, _chat_type, chat_id = telepot.glance(msg)
        self.valid =  msg_type == 'text'
        if self.valid:
            parser = UBParser(msg['text'])
            self.valid = self.valid and parser.valid()
        self.index = int(msg['message_id'])-INDEX_START
        print(self.index)
        if not self.valid:
            self.valid = (self.index % 37) == 0
        self.reply_to = msg['message_id']

    def response_url(self):
        with urllib.request.urlopen(URL) as response:
            html = response.read().decode('utf-8')
            urls = REGEXP.findall(html)
            if len(urls):
                url = urls.pop()
            else:
                url = 'https://media.tits-guru.com/images/ca456ca2-0409-4f99-a0fd-8a1d2de953ad.jpeg'
        return url

    def response_params(self):
        return {'disable_notification': True, 'reply_to_message_id': self.reply_to, 'caption': 'I think you secretly desired something like that'}
