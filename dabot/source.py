import time
import telepot
from telepot.loop import MessageLoop

from responders.complex_coordinates_responder import ComplexCoordinatesResponder
from responders.ubresponder import UBResponder
from responders.unsplashr import UnsplashResponder

from settings import TOKEN, ALLOWED, UNSPLASH_KEY
from pyunsplash import PyUnsplash

BOT = telepot.Bot(TOKEN)
API = PyUnsplash(api_key=UNSPLASH_KEY)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # ACL check: only specific chats are allowed
    if chat_id not in ALLOWED.keys():
        print('Filtered: ', content_type, chat_type, chat_id)
        return
    else:
        print('Received: ', content_type, ALLOWED[chat_id])
        
    # Responders are classes that respond to msg-s

    cListener = ComplexCoordinatesResponder(msg)
    if cListener.valid:
        # msg = cListener.response_msg()
        # print('cL:', msg)
        BOT.sendMessage(chat_id, cListener.response_msg(), **cListener.response_params())

    ubListener = UBResponder(msg)
    if ubListener.valid:
        print('Unexpected Boobs')
        BOT.sendPhoto(chat_id, ubListener.response_url(), **ubListener.response_params())

    unListener = UnsplashResponder(msg, API)
    if unListener.valid:
        print('Unsplash Image')
        BOT.sendPhoto(chat_id, unListener.response_url(), **unListener.response_params())
    #cListener = SimplePhotoUrlFetcher(msg)
    #if cListener.valid:
    #    BOT.sendPhoto(chat_id, cListener.response_msg(), **cListener.response_params())


MessageLoop(BOT, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(5)
