import xml.etree.ElementTree

def parseXml(data):
    if len(data) == 0:
        return  None
    xmlData = xml.etree.ElementTree.fromstring(data)
    msgType = xmlData.find('MsgType').text
    if msgType == "text":
        return TextMessage(xmlData)
    elif msgType == "image":
        return ImageMessage(xmlData)

class Message(object):
    def __init__(self):
        ## msg short for message
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgID = xmlData.find('MsgId').text

class TextMessage(Message):
    def __init__(self, xmlData):
        Message.__init__(self)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMessage(Message):
    def __init__(self, xmlData):
        Message.__init__(self)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text
