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
		print("||Web data:", webData)
		receivedMessage = receive.parseXml(webData)
		if isinstance(receivedMessage, receive.Message):
			toUser = receivedMessage.ToUserName
			fromUser = receivedMessage.FromUserName
			##guarder type if loops
			if receivedMessage.MsgType == "text":
				##not implemented
				##add gpt related functions here
				content = "test"
				replyMessage = reply.TextMessage(toUser, fromUser, content)
				replyMessage.send()
				return "<xml> <ToUserName><![CDATA[k740724287]]></ToUserName> <FromUserName><![CDATA[wx0699a80ad3228fe1]]></FromUserName><CreateTime>1460541339</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[test]]></Content></xml>"
			if receivedMessage.MsgType == "image":
				mediaId = receivedMessage.MediaId
				replyMessage = reply.ImageMessage(toUserName, fromUserName, mediaId)
				return replyMessage.send()
				return "success"
		return "success"