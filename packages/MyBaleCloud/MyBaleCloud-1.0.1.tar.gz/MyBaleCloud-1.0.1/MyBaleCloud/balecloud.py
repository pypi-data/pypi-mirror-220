# BackTrack
# python3
# HosT1LeT

import requests


print("""
\033[97mMyBaleCloud is \033[96mStarting\033[97m !

\033[97mpreparing to \033[91msetup \033[97mlibrary

""")


class BaleCloud:
    def __init__(self, botToken : str) -> None:
        self.token = str(botToken)
        global headers
        headers = {'Content-Type': 'Application/json', 'Accept': 'Application/json'}

    def sendMessage(self, message : str = None, chatID : str = None, messageID : str = None):
         
        if (message == None or chatID == None):
            raise ValueError('message or chatID argument cannot be empty')
        else:
            if messageID == None:
                req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendMessage?chat_id={chatID}&text={message}', headers=headers)

                return req.json()

            else:
                req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendMessage?chat_id={chatID}&text={message}&reply_to_message_id={messageID}',headers=headers)

                return req.json()

    def editMessageText(self, newMessage : str = None, chatID : str = None, messageID : str = None, ):
         
        if (newMessage == None or chatID == None or messageID == None):
            raise ValueError('newMessage / chatID / messageID cannot be empty')
        else:
            req = requests.get(f'https://tapi.bale.ai/bot{self.token}/editMessageText?chat_id={chatID}&text={newMessage}&message_id={messageID}',
            headers=headers)
            return req.json()

    def delMessage(self, chatID : str = None, messageID : str = None):
         
        if (chatID == None or messageID == None):
            raise ValueError('chatID or messageID argument cannot be empty')
        else:
            req = requests.post(f'https://tapi.bale.ai/bot{self.token}/deleteMessage', data={
                'chat_id' : str(chatID),
                'message_id' : object(messageID)
            },
            headers=headers)
            return req.json()

    def getUpdates(self, offset : int = 0, limit : int = 10):
         
        while 1:
            try:
                req = requests.post(f'https://tapi.bale.ai/bot{self.token}/getUpdates', data={
                    'offset' : int(offset),
                    'limit' : int(limit)
                },
                headers=headers)
                return req.json()
                break
            except:continue

    def setWebhook(self, url : str = None):
         
        if (url == None):
            raise ValueError('url argument cannot be empty')
        else:
            req = requests.post(f'https://tapi.bale.ai/bot{self.token}/setWebhook', data={
                'url' : url
            },
            headers=headers)

            return req

    def deleteWebhook(self):
         
        while 1:
            try:
                req = requests.get(f'https://tapi.bale.ai/bot{self.token}/deleteWebhook', headers=headers)
                return req.json()
                break
            except:continue


    def getMe(self):
         
        while 1:
            try:
                req = requests.post(f'https://tapi.bale.ai/bot{self.token}/getMe', headers=headers)
                return req
                break
            except:continue

    def sendPhoto(self, photoPathOrName : str = None, chatID : str = None, caption : str = '', messageID : str = None):
         
        if (photoPathOrName == None or chatID == None):
            raise ValueError('photoPath or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    with open(photoPathOrName, mode='rb') as MyPhoto:
                        req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendPhoto', data={
                            'chat_id' : int(chatID),
                            'photo' : MyPhoto,
                            'caption' : str(caption) if caption != None else '',
                            'reply_to_message_id' : object(messageID) if messageID != None else None or ''

                        }, headers=headers)
                        return req.json()
                        break
                except:continue

    def sendMp3(self, mp3filePathOrName : str = None, chatID : str = None, caption : str= None, messageID : str = None):
         
        if (mp3filePathOrName == None or chatID == None):
            raise ValueError('mp3filePath or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    with open(mp3filePathOrName, mode='rb') as MyMp3:
                        req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendAudio', data={
                            'chat_id' : int(chatID),
                            'audio' : MyMp3,
                            'caption' : str(caption) if caption != None else '',
                            'reply_to_message_id' : object(messageID) if messageID != None else None or ''
                        }, headers=headers)
                        return req.json()
                        break
                except:continue

    def sendDocument(self, docPathOrName : str = None, chatID : str = None, caption : str = None, messageID : str = None):
         
        if (docPathOrName == None or chatID == None):
            raise ValueError('docPath or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    with open(docPathOrName, mode='rb') as MyDoc:
                        req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendDocument', data={
                            'chat_id' : int(chatID),
                            'document' : MyDoc,
                            'caption' : str(caption) if caption != None else '',
                            'reply_to_message_id' : object(messageID) if messageID != None else '' or None
                        }, headers=headers)
                        return req.json()
                        break
                except:continue

    def sendVideo(self, videoPathOrName : str = None, chatID : str = None, caption : str = None, messageID : str = None):
         
        if (videoPathOrName == None or chatID == None):
            raise ValueError('videoPath or chatID argument cannot be empty')
        else:
            while 1:
                try:
                    with open(videoPathOrName, mode='rb') as MyVid:
                        req = requests.post(f'https://tapi.bale.ai/bot{self.token}/sendVideo', data= {
                            'chat_id' : int(chatID),
                            'video' : MyVid,
                            'caption' : str(caption) if caption != None else '',
                            'reply_to_message_id' : object(messageID) if messageID != None else '' or None
                        }, headers=headers)
                        return req.json()
                        break
                except:continue

    def getFile(self, fileID : str = None):
         
        if (fileID == None):
            raise ValueError('fileID argument cannot be empty')
        else:
            while 1:
                try:
                    return requests.get(f'https://tapi.bale.ai/bot{self.token}/getFile', data={
                        'file_id' : str(fileID)
                    }, headers=headers).json()
                    break
                except:continue

    def getChat(self, chatID : str = None):
         
        if (chatID == None):
            raise ValueError('chatID argument cannot be empty')
        else:
            while 1:
                try:
                    return requests.get(f'https://tapi.bale.ai/bot{self.token}/getChat?chat_id={str(chatID)}').json()
                    break
                except:continue

    def getChatAdministrators(self, chatID : str = None):
         
        if (chatID == None):
            raise ValueError('chatID argument cannot be empty')
        else:
            while 1:
                try:
                    return requests.get(f'https://tapi.bale.ai/bot{self.token}/getChatAdministrators?chat_id={str(chatID)}').json()
                    break
                except:continue

    def getChatMembersCount(self, chatID : str = None):
         
        if (chatID == None):
            raise ValueError('chatID argument cannot be empty')
        else:
            while 1:
                try:
                    return requests.get(f'https://tapi.bale.ai/bot{self.token}/getChatMembersCount?chat_id={str(chatID)}').json()
                    break
                except:continue

    def getChatMember(self, chatID : str = None, userID : str = None):
         
        if (chatID == None or userID == None):raise ValueError('chatID or userID argument cannot be empty')
        else:
            while 1:
                try:
                    return requests.get(f'https://tapi.bale.ai/bot{self.token}/getChatMember?chat_id={str(chatID)}&user_id={str(userID)}').json()
                    break
                except:continue
                
                
    def getLastUpdates(self, offset : int = 0, limit : int = 0):
         
        while 1:
            try:
                req = requests.post(f'https://tapi.bale.ai/bot{self.token}/getUpdates', data={
                    'offset' : int(offset),
                    'limit' : int(limit)
                },
                headers=headers)
                return (req.json())['result'][-1]
                break
            except:continue
            
    