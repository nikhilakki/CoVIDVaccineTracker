import requests
import json
import telegram

token = "YOUR_TOKEN"
url = "https://api.telegram.org/bot" + token


def send_mess(text):
    params = {"chat_id": "YOUR_CHAT_ID", "text": text}
    response = requests.post(url + "/sendMessage", data=params)
    resp_dict = json.loads(response.text)
    if resp_dict.get("ok"):
        return True, None
    else:
        return False, int(resp_dict["parameters"]["retry_after"])


def send_personal_message(msg, chat_id):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)
