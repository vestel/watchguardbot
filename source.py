import math
import sys
import time
import re
import telepot
from telepot.loop import MessageLoop
from settings import TOKEN


def waze_link(lat, lon):
    return "[Waze](https://www.waze.com/location?ll=%s,%s&navigate=yes)" % (lon, lat)

def gmaps_link(lat, lon):
    return "[GMaps](https://www.google.com/maps/search/?api=1&query=%s,%s)" % (lat, lon)

def osmand_link(lat, lon):
    return "[Osmand](https://osmand.net/go?lat=%s&lon=%s&z=16)" % (lat, lon)

def bing_link(lat, lon):
    return "[Bing](https://www.bing.com/maps/?v=2&cp=%s~%s&lvl=17&dir=0&sty=c&sp=point.%s_%s_Object)" % (lat, lon, lat, lon)

def bmaps_link(lat, lon):
    return "[BMaps](https://balticmaps.eu/map/?lat=%s&lon=%s&color=red)"%(lat,lon)


def sanitize_coordinate(coordinate):
    res = coordinate.replace(' ','.')
    res = res.replace(',','.')
    return res

def prepare_response(num, coordinates):
    lat, lon = coordinates
    return 'Uwaga! #%d (%s, %s) %s %s %s %s %s' % (num, lat, lon, waze_link(lat,lon), gmaps_link(lat, lon), osmand_link(lat, lon), bing_link(lat,lon), bmaps_link(lat,lon)) 

REGEXP = re.compile(r'.*?N?(\d{2}[\.|,|\s]\d{4,})N?[;|\s|,|\.]{1,10}E?(\d{2}[\.|,|\s]\d{4,})E?.*?')
class CoordinatesParser(object):
    def __init__(self, msg_text):
        self.matches = REGEXP.findall(msg_text)

    def valid(self):
        return len(self.matches)>0

    def normalize(self):
        return self.matches


class CoordinatesResponse(object):
    def __init__(self, msg_text, msg_type):
        self.valid =  msg_type == 'text'
        parser = CoordinatesParser(msg_text)
        self.valid = self.valid and parser.valid()
        if self.valid:
            self.coords = parser.normalize()

    def responseMsg(self): 
        text = ''
        for idx, coordinates in enumerate(self.coords):
            lat = sanitize_coordinate(coordinates[0])
            lon = sanitize_coordinate(coordinates[1])
            # TODO Flip coordinates during check in case of incorrect order
            if math.trunc(float(lat)) in range(50, 61) and math.trunc(float(lon)) in range(18,29):
                text += prepare_response(idx+1, (lat, lon))+'\n\n'
        return text

    def responseParams(self, reply):
        return {'parse_mode': 'Markdown', 'disable_web_page_preview': True, 'reply_to_message_id': reply}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    cListener = CoordinatesResponse(msg['text'], content_type)
    if cListener.valid:
        bot.sendMessage(chat_id, cListener.responseMsg(), **cListener.responseParams(msg['message_id']))

#    lListener = LursoftResponse(msg['text'])
#    if lListener:
#        bot.sendMessage(chat_id, lListener.responseToMsg(msg['text']), *lListener.responseParams())


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(5)
