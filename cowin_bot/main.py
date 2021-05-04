from utils.external_caller import APIInterface
import json
import pandas as pd
from utils.load_config import load_configuration
import os
from utils.get_state_id import (
    get_state_id_by_state_name,
    get_district_id_from_file,
    get_applicable_slots,
)
from utils.send_email import send_email_wrapper
from datetime import datetime

today = datetime.now()
print(f"New job started at {today}")
start_date = today.strftime("%d-%m-%Y")
config = load_configuration(config_path="data/config.yml")
get_slot_by_district = config.get("COWIN").get("SLOT_BY_DISTICT")
get_slot_by_pin = config.get("COWIN").get("SLOT_BY_PINCODE")
# user_details = load_configuration(config_path="data/user_details.yml")
# user_details = pd.read_csv("data/Contact Information.csv")
user_details = pd.read_csv("data/Contact Information.csv")
for user in user_details.itertuples(index=True, name="Pandas"):
    user_name = user.Name
    user_emailId = user.Email
    user_state = user.State
    user_district = user.District
    user_pincode = user.Pincode
    age_group = user._6.split("+")[0]
    try:
        district_id = ""
        state_id = get_state_id_by_state_name(state_name=user_state)
        if os.path.isfile(f"data/district_data/{state_id}.json"):
            district_id = get_district_id_from_file(
                file_path=f"data/district_data/{state_id}.json",
                district_name=user_district,
            )
        else:
            get_district_url = config.get("COWIN").get("GET_ALL_DISTICTS")
            district_obj = json.loads(
                APIInterface().get(route=f"{get_district_url}/{state_id}")
            )
            for dist in district_obj.get("districts"):
                if dist.get("district_name") == user_district:
                    district_id = dist.get("district_id")
            with open(f"data/district_data/{state_id}.json", "w") as f:
                json.dump(district_obj, f)
        slot_details = json.loads(
            APIInterface.get(
                route=get_slot_by_district,
                params={"district_id": district_id, "date": start_date},
            )
        )
        print(
            f"User Name: {user_name}, User Email: {user_emailId}, State Id: {state_id}, District Id: {district_id}, Age Group: {age_group}+"
        )
        available_slots = get_applicable_slots(
            slot_details=slot_details, age_group=age_group
        )
        if len(available_slots) > 0:
            print("slot available")
            success = send_email_wrapper(
                receiver_email=user_emailId,
                appointment_details=available_slots,
                name=user_name,
            )
            if success:
                print(f"Email sent to :{user_emailId}")
    except Exception as error:
        print(f"Error for user : {user_name}. Error : {error}")
        continue