import re

REGEXP = re.compile(r'.*?N?(\d{2}[\.|,|\s]\d{4,})N?[;|\s|,|\.]{1,10}E?(\d{2}[\.|,|\s]\d{4,})E?.*?')
class SimpleCoordinatesParser(object):
    def __init__(self, msg_text):
        self.raw_matches = REGEXP.findall(msg_text)

    def valid(self):
        return len(self.raw_matches)>0

    def normalize(self):
        res = []
        for lat, lon in self.raw_matches:
            slat = lat.replace(' ','.').replace(',','.')
            slon = lon.replace(' ','.').replace(',','.')
            res.append((slat, slon))
        return res
