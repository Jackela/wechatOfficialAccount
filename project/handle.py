import web
import hashlib
import receive
import reply
import openai
import chatBot
import os
import json
openai.api_key = "Replace"
openai.api_key = ""  # intialize global api key var
# Get the directory where chatBot.py is located
chatbot_directory = os.path.dirname(os.path.abspath(__file__))

# Get the relative path from chatBot.py to config.json
config_path = os.path.join(chatbot_directory, 'config.json')

def initialize_api_key():
    with open(config_path) as config:
        config = json.load(config)
        openai.api_key = config["openAI"]["apiKey"]

initialize_api_key()

class Handle(object):
	def GET(self):
		token = "OneToken"
		data = web.input()
		if len(data) ==0:
			return "ZERO"
		sha1 = hashlib.sha1()
		print(sha1.hexdigest())
		authList = [token, data.timestamp, data.nonce]
		authList.sort()
		for i in authList:
			sha1.update(i.encode('utf-8'))
		hashcode = sha1.hexdigest()
		print("handle/GET: {},  {}".format(hashcode, data.signature))
		if hashcode == data.signature:
			return data.echostr
		else:
			return "Check Signature"
	
	def POST(self):
		
		webData = web.data()
		print("||Web data:", webData)
		receivedMessage = receive.parseXml(webData)
		if isinstance(receivedMessage, receive.Message):
			##swap to and from user 
			##发信收信双方角色对调
			toUser = receivedMessage.FromUserName
			fromUser = receivedMessage.ToUserName
			##guarder type if loops
			if receivedMessage.MsgType == "text":
				##not implemented
				##add gpt related functions here
				print("received: ", receivedMessage.Content)
				##content = "As an AI language model, I cannot have personal opinions. However, according to statistics, Michael Jordan is widely considered one of the greatest basketball players of all time. Other players such as LeBron James, Kobe Bryant, Kareem Abdul-Jabbar, and Magic Johnson are also highly regarded. Ultimately, who is considered the best player depends on personal preference."
				content = chatBot.create_chat_completion(receivedMessage.Content.decode("utf-8"))
				replyMessage = reply.TextMessage(toUser, fromUser, content)
				print("sent: ", content)
				return replyMessage.send()

			if receivedMessage.MsgType == "image":
				mediaId = receivedMessage.MediaId
				replyMessage = reply.ImageMessage(toUserName, fromUserName, mediaId)
				return replyMessage.send()
		return "success"