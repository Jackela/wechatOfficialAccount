import web
import hashlib
import receive
import reply
import openai
from chatBot import OpenAIChatbot
openai.api_key = "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"

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
				chatbot = OpenAIChatbot()
				print("received: ", receivedMessage.Content)
				content = chatbot.generate_response(receivedMessage.Content.toString())
				replyMessage = reply.TextMessage(toUser, fromUser, content)
				return replyMessage.send()

			if receivedMessage.MsgType == "image":
				mediaId = receivedMessage.MediaId
				replyMessage = reply.ImageMessage(toUserName, fromUserName, mediaId)
				return replyMessage.send()
		return "success"