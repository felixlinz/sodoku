import json
import requests
import datetime
import re
import csv
import time
from sudokuchat import Board as Board
from sudokuchat import solve as solve
from sudokuchat import getsudoku as getsudoku



class ultraChatBot():    
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance49996/'
        self.token = 'vyijsik2q818dbyp'

   
    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to" : chatID,
                "body" : text}  
        answer = self.send_requests('messages/chat', data)
        return answer

    def processingـincomingـmessages(self):
        message = self.dict_messages
        text = message["body"].lower()
        chatID = message["from"]
        match = re.search(r"^(sudoku)", text)
        if match:
            return "input sudoku all at once, replace"
        else: 
            attempt = re.search(r'^\d{9}$', text)
            if attempt:
                return self.send_message(chatID,"Fermentation Chamber Please type one of these commands: *ferment* + \n*set temp- ?* \n*set temp- ?*\n*set humidity- ?*\n*set duration- ?*\n*turn off-*\n*conditions-*\n*set vent- ?*\n*Avoid any °C, % or other Symbols*")