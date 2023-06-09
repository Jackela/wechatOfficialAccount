import json
import base64
import os
import requests
import accesstoken
import requests
## for testing
import chatbot
directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(directory, 'image.jpg')
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
    with open(file_path, "wb") as f:
        f.write(response.content)
    return file_path
    

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
    url_to_image(chatbot.create_image("A running cat"))
