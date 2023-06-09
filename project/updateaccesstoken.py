## 这是一个定时运行的任务，用于更新access_token
import os
import time
import accesstoken
import json
now = time.time()
directory = os.path.dirname(os.path.abspath(__file__))
access_token_path = os.path.join(directory, 'access_token.json')
def initialize_token():
    with open(access_token_path, 'r') as f:
        config = json.load(f)
        access_token, expires_at = config['access_token'], config['expires_at']

        return access_token, expires_at

access_token, expires_at = initialize_token()

## if token has expired
if expires_at <= now:
    accesstoken.getAccessToken()
