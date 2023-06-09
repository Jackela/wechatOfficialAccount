import web
import hashlib
import receive
import reply
import openai
import os
import json
import imageutils
import accesstoken
import chatbot
import asyncio
# Get the directory where chatbot.py is located
directory = os.path.dirname(os.path.abspath(__file__))

# Get the relative path from chatbot.py to config.json
config_path = os.path.join(directory, 'config.json')

access_token = accesstoken.get_current_access_token()

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
				response = chatbot.response_to_user(receivedMessage.Content.decode("utf-8"))
				print("sent: ", response)
				if clarified_type == "chat":
					replyMessage = reply.TextMessage(toUser, fromUser, response)
					return replyMessage.send()
				elif clarified_type == "image":
					asyncio.create_task(chatbot.send_image(receivedMessage.Content, toUser))
					replyMessage = reply.TextMessage(toUser, fromUser, response)
					return replyMessage.send()

		return "success"