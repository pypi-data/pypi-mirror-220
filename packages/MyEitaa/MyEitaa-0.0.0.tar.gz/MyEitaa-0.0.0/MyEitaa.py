import requests
from bs4 import BeautifulSoup

class ClientEitaa:
    def __init__(self, api : str =None) -> None:
        self.api = str(api)
        

    def sendMessage(self, message = None, chatID = None, replyToMsgId = None, pin=False, sendNotification = True):
        if self.api == None:
            return 'api cannot be empty'
        else:
            if (chatID == None or message == None):
                return 'some arguments is empty, the library cannot perparing with empty arguments\nargumants {\nchatID\nmessage\n}'
            
            else:
                Data = {
                    'chat_id' : chatID,
                    'text' : message,
                    'pin' : pin,
                    'disable_notification': sendNotification,
                    'reply_to_message_id' : replyToMsgId if replyToMsgId != None else ''
                }
                req = requests.post(url=f'https://eitaayar.ir/api/{self.api}/sendMessage', data=Data).json
                return req
            
    
    def sendPhoto(self, photoName : str = None,chatID = None, caption : str = None, pin = False, replyToMsgId = None, sendNotification = True):
        if self == None:
            return 'api cannot be empty'
        else:
            if (photoName == None or chatID == None):
                return 'some arguments is empty, the library cannot perparing with empty arguments\nargumants {\nchatID\nphoto\n}'
            else:
                Data = {
                    'chat_id' : chatID,
                    'caption' : caption,
                    'pin' : pin,
                    'disable_notification': sendNotification,
                }
                
                with open(photoName, 'rb') as MyPhoto:
                    
                    req = requests.post(f'https://eitaayar.ir/api/{self.api}/sendFile',
                        data = {
                            'chat_id' : chatID,
                            'caption' : caption if caption != None else '' ,
                            'pin' : pin,
                            'disable_notification': sendNotification,
                            'reply_to_message_id' : replyToMsgId if replyToMsgId != None else '',
                    },
                            
                        files = {
                            'file' : MyPhoto
                        }
                    )
                    return req.json
                
    def sendDocument(self, docName : str = None, chatID = None, replyToMsgId = None, caption : str = None, sendNotification = True):
        if self.api == None:
            return 'api cannot be empty'
        else:
            if (docName == None or chatID == None):
                return 'some arguments is empty, the library cannot perparing with empty arguments\nargumants {\nchatID\ndocName\n}'
            else:
                req = requests.post(f'https://eitaayar.ir/api/{self.api}/sendFile', 
                    data = {
                        'chat_id' : chatID,
                        'caption' : caption if caption != None else '',
                        'disable_notification' : sendNotification,
                        'reply_to_message_id' : replyToMsgId if replyToMsgId != None else ''
                    },
                    files= {
                        'file' : open(docName, 'rb')
                    }
                )
                return req.json
                
    def sendMediaFromTxtFile(self, fileName = None, chatID = None, replyToMsgId = None, sendNotification = True):
        if self.api == None:
            return 'api cannot be empty'
        else:
            if (fileName == None or chatID == None):
                return 'some arguments is empty, the library cannot perparing with empty arguments\nargumants {\nchatID\ndocName\n}'
            else:
                readFile = open(fileName, 'r').read()
                req = requests.post(f'https://eitaayar.ir/api/{self.api}/sendText', 
                    data = {
                        'chat_id' : chatID,
                        'text' : str(readFile),
                        'disable_notification' : sendNotification,
                        'reply_to_message_id' : replyToMsgId if replyToMsgId != None else ''
                    }
                )
                return req.json
            
            
    # Im copy paste this method (getTrends) from eitaa library
    def getTrends():
        result = {
            "last_12_hours": [],
            "last_24_hours": [],
            "last_7_days": [],
            "last_30_days": [],
        }

        r = requests.get(
            f"https://trends.eitaa.com"
        )

        soup = BeautifulSoup(r.text, 'html.parser')

        last_12_hours = soup.find("div",{"class":"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInLeft"})
        last_24_hours = soup.find("div",{"class":"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInDown"})
        last_7_days = soup.find("div",{"class":"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInRight"})
        last_30_days = soup.find("div",{"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInUp"})

        # پردازش هشتگ های ترند شده در 12 ساعت گذشته
        for trend in last_12_hours.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_12_hours"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })

        # پردازش هشتگ های ترند شده در روز گذشته
        for trend in last_24_hours.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_24_hours"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })
        
        # پردازش هشتگ های ترند شده در هفت روز گذشته
        for trend in last_7_days.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_7_days"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })
        
        # پردازش هشتگ های ترند شده در 30 روز گذشته
        for trend in last_30_days.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_30_days"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })
        return result
