import web
import hashlib
import receive
import reply


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
		print("web data:", webData)
		receivedMessage = receive.parseXml(webData)
		if isinstance(receivedMessage, receive.Message):
			toUser = receivedMessage.toUserName
			fromUser = receivedMessage.FromUserName
			##guarder type if loops
			if receivedMessage.MsgType == "text":
				##not implemented
				##add gpt related functions here
				content = "怎么你了"
				replyMessage = reply.TextMessage(toUserName, tromUserName, content)
				return replyMessage.send()
			if receivedMessage.MsgType == "image":
				mediaId = receivedMessage.MediaId
				replyMessage = reply.ImageMessage(toUserName, fromUserName, mediaId)
				return replyMessage.send()