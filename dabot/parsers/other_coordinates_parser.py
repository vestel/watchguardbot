import re

REGEXP = re.compile(r'.*?(\d{2}°\s?\d{2}\'\s?\d{2}")\s?[N|E]\s{1,5}(\d{2}°\s?\d{2}\'\s?\d{2}")\s?[N|E].*?')
SUBRE = re.compile(r'(\d{2})°(\d{2})\'(\d{2})"')
class OtherCoordinatesParser(object):
    def __init__(self, msg_text):
        msg_text = msg_text.replace('′','\'').replace('″','"')
        self.raw_matches = REGEXP.findall(msg_text)

    def valid(self):
        return len(self.raw_matches)>0

    def normalize(self):
        res = []
        for lat, lon in self.raw_matches:
            slat = lat.replace(' ','')
            degrees, minutes, seconds = SUBRE.findall(slat).pop()
            mlat = round(int(degrees) + (int(minutes)/60.0) + (int(seconds)/3600.0), 6)
            slon = lon.replace(' ','')
            degrees, minutes, seconds = SUBRE.findall(slon).pop()
            mlon = round(int(degrees) + (int(minutes)/60.0) + (int(seconds)/3600.0), 6)
            res.append((mlat, mlon))
        return res
