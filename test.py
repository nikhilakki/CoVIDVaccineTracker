import json
from datetime import datetime

today_date = datetime.today().date()
print(today_date)
with open(
    "/Users/arpitkjain/Desktop/Data/POC/cowin/cowin_bot/data/mail_sent_data.json", "r"
) as f:
    data = json.load(f)
    print(data)
email_sent_to = [key for key in data.keys()]
email = "arpitjain@gmail.com"
date = data.get(email, None)
print(date)
if date is not None:
    if date != str(today_date):
        print("send email")
        data.update({email: str(today_date)})
else:
    print("send email")
    data.update({email: str(today_date)})
with open(
    "/Users/arpitkjain/Desktop/Data/POC/cowin/cowin_bot/data/mail_sent_data.json",
    "w",
) as f:
    json.dump(data, f)
