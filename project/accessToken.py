import requests
import time


appid = "wx0699a80ad3228fe1"
appsecret = "c59d59e306c6dfad3d3c643ce7af07b6"
url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}".format(APPID = appid , APPSECRET = appsecret)
##the redundance of timeout is to avoid the situation that the token expires before the request is sent
timeoutRedundance = 10
def getAccessToken():
    response = requests.get(url).json()
    return AccessToken(response['access_token'], response['expires_in'])


class AccessToken(object):
    def __init__(self):
        self.__accessToken = ""
        self.__leftTime = 0
        self.__expireTime = 0
        self.countDown()

    def __init__(self, accessToken, expireIn):
        self.__accessToken = accessToken
        self.__leftTime = expireIn
        self.__expireTime = expireIn
        print (accessToken)
        self.countDown()

    def isTimeout(self):
        return self.__leftTime <= 0 + timeoutRedundance


    def refreshAccessToken(self):
        response = requests.get(url).json()
        self.__init__(response['access_token'], response['expires_in'])
    
    def countDown(self):
        while not self.isTimeout():
            self.__leftTime -= 5
            time.sleep(5)
            self.getTimeLeft()
        self.refreshAccessToken()
        countDown()

    ##for testing
    def getTimeLeft(self):
        print(self.__leftTime)
    def getAccessToken(self):
        return self.__accessToken

if __name__ == "__main__":
    print(getAccessToken().getAccessToken())