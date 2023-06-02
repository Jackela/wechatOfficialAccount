import time

class Message:
    def __init__(self):
        self.ToUserName = ""
        self.FromUserName = ""
        self.CreateTime = int(time.time())
        self.MsgType = ""
        self.MsgId = 0
    
    def send(self):
        return "success"

class TextMessage:
    def __init__(self, toUserName, fromUserName, content):
        self.messageDictionary = dict()
        self.messageDictionary['ToUserName'] = toUserName
        self.messageDictionary['FromUserName'] = fromUserName
        self.messageDictionary['CreateTime'] = int(time.time())
        self.messageDictionary['MsgType'] = "text"
        self.messageDictionary['Content'] = content

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[{MsgType}]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return XmlForm.format(**self.messageDictionary)


        
    
class ImageMessage:
    def __init__(self, toUserName, fromUserName, MediaId):
        self.messageDictionary = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MsgType'] = "image"
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Image>
            </xml>
            """
        return XmlForm.format(**self.messageDictionary)