import math
import sys
import time
import re
import telepot
from telepot.loop import MessageLoop
from settings import TOKEN

REGEXP = re.compile(r'.*?N?(\d{2}[\.|,|\s]\d{4,})N?[;|\s|,|\.]{1,10}E?(\d{2}[\.|,|\s]\d{4,})E?.*?')

def waze_link(lat, lon):
    return "[Waze](https://www.waze.com/location?ll=%s,%s&navigate=yes)" % (lat, lon)

def gmaps_link(lat, lon):
    return "[GMaps](https://www.google.com/maps/search/?api=1&query=%s,%s)" % (lat, lon)

def osmand_link(lat, lon):
    return "[Osmand](https://osmand.net/go?lat=%s&lon=%s&z=16)" % (lat, lon)

def bing_link(lat, lon):
    return "[Bing](https://www.bing.com/maps/?v=2&cp=%s~%s&lvl=17&dir=0&sty=c&sp=point.%s_%s_Object)" % (lat, lon, lat, lon)

def sanitize_coordinate(coordinate):
    res = coordinate.replace(' ','.')
    res = res.replace(',','.')
    return res

def prepare_response(num, coordinates):
    lat, lon = coordinates
    return 'Uwaga! #%d (%s, %s) %s %s %s %s' % (num, lat, lon, waze_link(lat,lon), gmaps_link(lat, lon), osmand_link(lat, lon), bing_link(lat,lon)) 

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        matches = REGEXP.findall(msg['text'])
        for idx, coordinates in enumerate(matches):
            lat = sanitize_coordinate(coordinates[0])
            lon = sanitize_coordinate(coordinates[1])
            if math.trunc(float(lat)) in range(50, 61) and math.trunc(float(lon)) in range(18,29):
                bot.sendMessage(chat_id, prepare_response(idx+1, (lat, lon)), parse_mode='Markdown', disable_web_page_preview=True, reply_to_message_id=msg['message_id'])


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(5)
