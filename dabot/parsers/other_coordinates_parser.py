import re

REGEXP = re.compile(r'.*?N?\s?(\d{1,3}°\s?\d{2}\'\s?\d{2}")\s?N?i[\s|,|\.|;]{1,5}E?\s?(\d{1,3}°\s?\d{2}\'\s?\d{2}")\s?E?.*?')
SUBRE = re.compile(r'(\d{1,3})°(\d{2})\'(\d{2})"')
class OtherCoordinatesParser(object):
    def __init__(self, msg_text):
        msg_text = msg_text.replace('′','\'').replace('″','"').replace('”','"').replace('’','\'')
        print('ÓCP:', msg_text)
        self.raw_matches = REGEXP.findall(msg_text)
        print('ÓCP:', self.raw_matches)

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
        print("OCP:", res)
        return res
