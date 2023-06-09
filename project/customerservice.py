import requests
import json
import accesstoken
def add_custom_service_account(kf_account, nickname, password):
    url = 'https://api.weixin.qq.com/customservice/kfaccount/add?access_token='+ accesstoken.get_current_access_token()
    headers = {'Content-Type': 'application/json'}
    data = {
        "kf_account" : kf_account,
        "nickname" : nickname,
        "password" : password
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        if result['errcode'] == 0:
            print('添加客服账号成功！')
        else:
            print('添加客服账号失败，错误码：{}，错误信息：{}'.format(result['errcode'], result['errmsg']))
    else:
        print('添加客服账号失败，http状态码：{}'.format(response.status_code))

if __name__ == "__main__":
    add_custom_service_account('test1@test', '客服1', 'password')