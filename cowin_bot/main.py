import json
from utils.load_config import load_configuration
from datetime import datetime
from utils.api_call import get_details, trigger_api_setu
from VacciDate_bot.update_db import get_all
from integration.api_setu import get_generic_slots
from VacciDate_bot.send_message import send_personal_message

today = datetime.now()
print(f"New job started at {today}")
start_date = today.strftime("%d-%m-%Y")
config = load_configuration(config_path="data/config.yml")
get_slot_by_district = config.get("COWIN").get("SLOT_BY_DISTICT")
get_slot_by_pin = config.get("COWIN").get("SLOT_BY_PINCODE")
data = get_all()
dist_set = {}
for rec in data:
    if len(rec[4]) > 3:
        for d_id in rec[4].split(","):
            user_list = dist_set.get(d_id, None)
            if user_list is None:
                user_list = [rec[3]]
                dist_set.update({d_id: user_list})
            else:
                user_list.append(rec[3])
                dist_set.update({d_id: user_list})
    else:
        user_list = dist_set.get(rec[4], None)
        if user_list is None:
            user_list = [rec[3]]
            dist_set.update({rec[4]: user_list})
        else:
            user_list.append(rec[3])
            dist_set.update({rec[4]: user_list})
for dist in dist_set.items():
    try:
        dist_code = dist[0]
        slot_details = trigger_api_setu(district_id=dist_code, start_date=start_date)
        available_slots = get_generic_slots(slot_details)
        if len(available_slots) > 0:
            print(f"slot available in {dist_code}")
            for chat_id in dist[1]:
                for i in range(min(5, len(available_slots))):
                    success = send_personal_message(
                        msg=available_slots[i], chat_id=chat_id
                    )
                    if not success:
                        break
    except Exception as error:
        print(f"Error in main.py : {error}")
        continue
