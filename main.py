"""

import time
import sys
from bots import bot

def main():
  while 1:
     import bot
     try:
        bot.app.polling(timeout=60)
     except Exception as e:
        del sys.modules['bot']
        del sys.modules['remain_up']
        time.sleep(5)

main()
"""