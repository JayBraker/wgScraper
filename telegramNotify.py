#!/home/jaybraker/wgSuche/bin/python
import telegram
import json

class notify:
    def __init__(self, token, target):
        self.bot = telegram.Bot(token)
        self.target = target

    def send(self, msg):
        if msg:
            self.bot.send_message(chat_id = self.target, text = msg, parse_mode = telegram.ParseMode.HTML)
