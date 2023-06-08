import web
import hashlib
import receive
import reply
import openai
import chatBot
import os
import json
import imageUtils
import accessToken
# Get the directory where chatBot.py is located
directory = os.path.dirname(os.path.abspath(__file__))

# Get the relative path from chatBot.py to config.json
config_path = os.path.join(directory, 'config.json')

access_token = accessToken.getAccessToken()

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
				clarified_type, response = chatBot.response_to_user(receivedMessage.Content.decode("utf-8"))
				print("sent: ", clarified_type, response)
				if clarified_type == "text":
					replyMessage = reply.TextMessage(toUser, fromUser, content)
				elif clarified_type == "image":
					imageUtils.url_to_image(response, "temp.jpg")
					mediaId = imageUtils.upload_image("temp.jpg", accessToken.get_current_access_token())
					replyMessage = reply.ImageMessage(toUser, fromUser, mediaId)

				return replyMessage.send()


			if receivedMessage.MsgType == "image":
				mediaId = receivedMessage.MediaId
				replyMessage = reply.ImageMessage(toUserName, fromUserName, mediaId)
				return replyMessage.send()
		return "success"