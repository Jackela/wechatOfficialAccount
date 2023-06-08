import requests
import time
import json
import os

appid = ""
appsecret = ""
directory = os.path.dirname(os.path.abspath(__file__))
# Get the relative path from chatBot.py to config.json
config_path = os.path.join(directory, 'config.json')
access_token_path = os.path.join(directory, 'access_token.json')
def initialize_credentials():
    with open(config_path, 'r') as f:
        config = json.load(f)
        appid = config["wechat"]["appId"]
        appsecret = config["wechat"]["appSecret"]
        return appid, appsecret

appid, appsecret = initialize_credentials()

initialize_credentials()
url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}".format(APPID = appid , APPSECRET = appsecret)
##the redundance of timeout is to avoid the situation that the token expires before the request is sent
timeoutRedundance = 10
def getAccessToken():
    response = requests.get(url).json()
    access_token, expires_in = response['access_token'], response['expires_in']
    expires_at = time.time() + expires_in
    with open(access_token_path, 'w') as f:
        json.dump({'access_token': access_token, 'expires_at': expires_at}, f)
def get_current_access_token():
    with open(access_token_path, 'r') as f:
        access_token = f['access_token']
        return access_token
        
class AccessToken(object):
    def __init__(self):
        self.__accessToken = ""
        self.__expireTime = 0
        self.__expiresAt = time.time()

    def __init__(self, accessToken, expireIn):
        self.__accessToken = accessToken
        self.__expireTime = expireIn
        self.__expiresAt = time.time() + expireIn

    def isTimeout(self):
        return self.__expiresAt >= time.time() +  timeoutRedundance

    ## Deprecated
    def refreshAccessToken(self):
        response = requests.get(url).json()
        self.__init__(response['access_token'], response['expires_in'])
    

    ##for testing
    def __getExpireAt(self):
        print(self.__expireAt)
    def __getAccessToken(self):
        print(self.__accessToken)



if __name__ == "__main__":
    res = getAccessToken()
    
    print(res)
