import math
import sys
import time
import re
import telepot
from telepot.loop import MessageLoop

from responders.simple_coordinates_responder import SimpleCoordinatesResponder
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
    cListener = SimpleCoordinatesResponder(msg)
    if cListener.valid:
        BOT.sendMessage(chat_id, cListener.response_msg(), **cListener.response_params())

MessageLoop(BOT, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(5)
