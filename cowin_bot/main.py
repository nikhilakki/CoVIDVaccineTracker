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
data = json.load(open("data/check_status.json", "r"))
for district_id in data["district_list"]:
    get_details(district_id, start_date, 18)
