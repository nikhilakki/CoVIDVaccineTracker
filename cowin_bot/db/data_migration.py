import sqlite3
import json
from datetime import datetime

today = datetime.today()

conn = sqlite3.connect("vaccidate.db")
c = conn.cursor()
data = json.load(
    open(
        "/Users/arpitkjain/Desktop/Data/POC/CoVIDVaccineTracker/cowin_bot/data/user_data.json",
        "r",
    )
)
for user_data in data["user_data"].items():
    district = ",".join(user_data[1]["districts"])
    age_group = []
    for age in user_data[1]["age_groups"]:
        age_group.append(str(age))
    age_group = ",".join(age_group)
    sql = f"""INSERT INTO USERS(username,first_name,last_name,chat_id,district,age_group,timestamp)
              VALUES('{user_data[0]}','{user_data[1]['first_name']}','{user_data[1]['last_name']}',{user_data[1]['chat_id']},'{district}','{age_group}','{today}')"""
    print(sql)
    c.execute(sql)
    conn.commit()
