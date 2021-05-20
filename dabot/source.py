import time
import telepot
from telepot.loop import MessageLoop

from responders.complex_coordinates_responder import ComplexCoordinatesResponder
from responders.ubresponder import UBResponder
from responders.unsplashr import UnsplashResponder

from settings import TOKEN, ALLOWED, UNSPLASH_KEY, BOT_ADMINS, DEFAULT_FEATURES
from pyunsplash import PyUnsplash

BOT = telepot.Bot(TOKEN)
API = PyUnsplash(api_key=UNSPLASH_KEY)
currentFeatures = {}
for chat_id in list(ALLOWED.keys()):
    currentFeatures[chat_id] = DEFAULT_FEATURES

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # ACL check: only specific chats are allowed
    if chat_id not in ALLOWED.keys():
        print('Filtered: ', content_type, chat_type, chat_id)
        return
    else:
        print('Received: ', content_type, ALLOWED[chat_id])

    # Check if admin, fix current settings
    if msg['text'].startswith('`dbot_'):
        print(msg)
        if msg['from']['id'] in BOT_ADMINS[chat_id].values():
            print('AdminCommand:', msg)
            param = msg['text'].split('_')[1]
            try:
                key = param.split('=')[0]
                value = param.split('=')[1]
                print(currentFeatures[chat_id].get(key))
                currentFeatures[chat_id][key] = value == 'on'
            except IndexError:
                pass
            return

    # Responders are classes that respond to msg-s
    cListener = ComplexCoordinatesResponder(msg)
    if currentFeatures[chat_id][cListener.handle] and cListener.valid:
        # msg = cListener.response_msg()
        # print('cL:', msg)
        BOT.sendMessage(chat_id, cListener.response_msg(), **cListener.response_params())
        return

    ubListener = UBResponder(msg)
    if currentFeatures[chat_id][ubListener.handle] and ubListener.valid:
        print('Unexpected Boobs')
        BOT.sendPhoto(chat_id, ubListener.response_url(), **ubListener.response_params())
        return

    unListener = UnsplashResponder(msg, API)
    if currentFeatures[chat_id][unListener.handle] and unListener.valid:
        print('Unsplash Image')
        BOT.sendPhoto(chat_id, unListener.response_url(), **unListener.response_params())
        return
    #cListener = SimplePhotoUrlFetcher(msg)
    #if cListener.valid:
    #    BOT.sendPhoto(chat_id, cListener.response_msg(), **cListener.response_params())


MessageLoop(BOT, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(5)
