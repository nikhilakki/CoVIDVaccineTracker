import requests
import json

url = "bot url"


def send_mess(text):
    params = {"chat_id": "-1001177302753", "text": text}
    response = requests.post(url + "/sendMessage", data=params)
    resp_dict = json.loads(response.text)
    if resp_dict.get("ok"):
        return True, None
    else:
        return False, int(resp_dict["parameters"]["retry_after"])


# send_mess("Jalgon\nBhusawal\n45\nCOVAXIN")
