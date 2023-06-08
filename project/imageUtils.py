import json
import base64
import requests
import accessToken

#not tested
def b64_json_to_image(b64_json):
    # Decode the Base64 string into a UTF-8 encoded JSON string
    json_str = base64.b64decode(b64_json).decode('utf-8')

    # Parse the JSON string into a dictionary
    data = json.loads(json_str)

    # Extract the image data from the dictionary
    image_data = base64.b64decode(data['file_content'])

    # Write the image data to a file
    with open(data['test.png'], 'wb') as f:
        f.write(image_data)

def url_to_image(url:str, file_name:str="image.jpg"):
    response = requests.get(url)
    with open("project\{file_name}", "wb") as f:
        f.write(response.content)

import requests

def upload_image(access_token: str, filepath: str) -> str:
    url = "https://api.weixin.qq.com/cgi-bin/media/upload"
    params = {"access_token": access_token, "type": "image"}

    with open(filepath, "rb") as f:
        r = requests.post(url, params=params, files={"media": f})

    response = r.json()
    if "errcode" in response:
        error_msg = response.get("errmsg", "Unknown error")
        print(f"Error uploading image: {error_msg}")
        return ""
    else:
        media_id = response["media_id"]
        return media_id

if __name__ == "__main__":
    res = upload_image("69_s29otVCXu1Q97yB4hIxZV86AT3VkcFNWZz7NEYo3OyQQMj86pNmNfq2wjo4rF_OwRZUd9JvghkOnoMG9jG8dVMtFf53I0GxRUpcwFN6u6YsV_2cwyzcdMOCQ-9wBAMhAIAUTF", "project\image.png")
    print(res)