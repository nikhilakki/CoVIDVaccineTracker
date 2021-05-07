from utils.load_config import load_configuration
from datetime import datetime
from utils.api_call import trigger_api_setu
from integration.api_setu import get_generic_slots
from VacciDate_bot.send_message import send_mess
import time

today = datetime.now()
start_date = today.strftime("%d-%m-%Y")
config = load_configuration(config_path="data/config.yml")
get_slot_by_district = config.get("COWIN").get("SLOT_BY_DISTICT")
get_slot_by_pin = config.get("COWIN").get("SLOT_BY_PINCODE")
for i in range(3):
    try:
        print(f"New job started at {datetime.now()}")
        dist_code = "603"
        slot_details = trigger_api_setu(district_id=dist_code, start_date=start_date)
        available_slots = get_generic_slots(slot_details, age_group=18)
        if len(available_slots) > 0:
            print(f"slot available in {dist_code}")
            for i in range(min(5, len(available_slots))):
                success = send_mess(text=available_slots[i], dist_code=dist_code)
                if not success:
                    break
        time.sleep(20)
    except Exception as error:
        print(f"Error in main.py : {error}")
        continue
