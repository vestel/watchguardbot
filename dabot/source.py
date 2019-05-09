import time
import telepot
from telepot.loop import MessageLoop

from responders.complex_coordinates_responder import ComplexCoordinatesResponder
from settings import TOKEN, ALLOWED

BOT = telepot.Bot(TOKEN)

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

    #cListener = SimplePhotoUrlFetcher(msg)
    #if cListener.valid:
    #    BOT.sendPhoto(chat_id, cListener.response_msg(), **cListener.response_params())


MessageLoop(BOT, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(5)
