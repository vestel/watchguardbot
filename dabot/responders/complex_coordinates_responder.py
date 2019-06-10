import math
import telepot 

from parsers.simple_coordinates_parser import SimpleCoordinatesParser
from parsers.other_coordinates_parser import OtherCoordinatesParser
from settings import INDEX_START

class ComplexCoordinatesResponder(object):
    def __init__(self, msg):
        msg_type, _chat_type, chat_id = telepot.glance(msg)
        self.valid =  msg_type == 'text'
        if self.valid:
            parser = SimpleCoordinatesParser(msg['text'])
            self.valid = self.valid and parser.valid()
        if not self.valid:
            parser = OtherCoordinatesParser(msg['text'])
            self.valid = parser.valid()
        self.reply_to = msg['message_id']
        self.index = int(msg['message_id'])-INDEX_START
        if self.valid:
            self.coords = parser.normalize()

    def waze_link(self, lat, lon):
        #return "[Waze](https://www.waze.com/location?ll=%s,%s&navigate=yes)" % (lon, lat)
        return "[Waze](https://www.waze.com/location?ll=%s,%s&navigate=yes)" % (lat, lon)

    def gmaps_link(self, lat, lon):
        return "[GMaps](https://www.google.com/maps/search/?api=1&query=%s,%s)" % (lat, lon)

    def osmand_link(self, lat, lon):
        return "[OSM](https://osmand.net/go?lat=%s&lon=%s&z=16)" % (lat, lon)

    def bing_link(self, lat, lon):
        return "[Bing](https://www.bing.com/maps/?v=2&cp=%s~%s&lvl=17&dir=0&sty=c&sp=point.%s_%s_Object)" % (lat, lon, lat, lon)

    def bmaps_link(self, lat, lon):
        return "[Baltic](https://balticmaps.eu/map/?lat=%s&lon=%s&color=red&key=MK_464786&zoom=17)"%(lat,lon)

    def prepare_response(self, num, lat, lon):
        return '%d* (%s, %s) %s %s %s %s %s' % (num, lat, lon, 
            self.waze_link(lat,lon), self.gmaps_link(lat, lon), 
            self.osmand_link(lat, lon), self.bing_link(lat,lon), 
            self.bmaps_link(lat,lon)) 

    def response_msg(self):
        text = ''
        prefix = '*#%s.' % self.index
        for idx, coordinates in enumerate(self.coords):
            # TODO Flip coordinates during check in case of incorrect order
            lat, lon = coordinates
            if math.trunc(float(lat)) in range(50, 61) and math.trunc(float(lon)) in range(18,29):
                text += prefix + self.prepare_response(idx+1, lat, lon)+'\n\n'
            else:
                lon, lat = coordinates
                if math.trunc(float(lat)) in range(50, 61) and math.trunc(float(lon)) in range(18,29):
                    text += prefix + self.prepare_response(idx+1, lat, lon)+'\n\n'
                else:
                    text += prefix + str(idx+1)+'*: Ignored due to our of search zone'
        return text

    def response_params(self):
        return {'parse_mode': 'Markdown', 'disable_web_page_preview': True, 'reply_to_message_id': self.reply_to }
