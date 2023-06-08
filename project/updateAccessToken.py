## 这是一个定时运行的任务，用于更新access_token

import time
import accessToken

now = time.time()


def initialize_token():
    with open(access_token_path, 'r') as f:
        access_token, expires_at = f['access_token'], f['expires_at']
        return access_token, expires_at

accessToken, expires_at = initialize_token()

## if token has expired
if expires_at <= now():
    accessToken.getAccessToken()
