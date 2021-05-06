import json
from utils.load_config import load_configuration
from datetime import datetime
from utils.api_call import get_details

today = datetime.now()
print(f"New job started at {today}")
start_date = today.strftime("%d-%m-%Y")
config = load_configuration(config_path="data/config.yml")
get_slot_by_district = config.get("COWIN").get("SLOT_BY_DISTICT")
get_slot_by_pin = config.get("COWIN").get("SLOT_BY_PINCODE")
data = json.load(open("data/user_data.json", "r"))
for user in data["user_data"].items():
    chat_id = user[1].get("chat_id")
    dist_list = user[1].get("districts")
    age_group = user[1].get("age_groups")
    print(chat_id, dist_list, age_group)
    for district_id in dist_list:
        success = get_details(district_id, start_date, age_group, chat_id)
        if not success:
            continue
