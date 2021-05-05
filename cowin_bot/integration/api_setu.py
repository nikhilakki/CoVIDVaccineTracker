import json


def get_state_id_by_state_name(state_name: str):
    with open("data/state_code.json", "r") as f:
        data = json.load(f)
    not_found = False
    for state in data.get("states"):
        if state.get("state_name") == state_name:
            return state.get("state_id")
        else:
            not_found = True
            continue
    if not_found:
        return None


def get_district_id_from_file(file_path: str, district_name: str):
    with open(file_path, "r") as f:
        data = json.load(f)
    not_found = False
    for dist in data.get("districts"):
        if dist.get("district_name") == district_name:
            return dist.get("district_id")
        else:
            not_found = True
            continue
    if not_found:
        return None


def get_applicable_slots(slot_details: dict, age_group: int):
    master_list = []
    for slot in slot_details.get("centers"):
        if len(slot.get("sessions")) > 0:
            for session in slot.get("sessions"):
                if (
                    session.get("min_age_limit") == age_group
                    and session.get("available_capacity") > 0
                ):
                    # booking_details = {
                    #     "Center Name": slot.get("name"),
                    #     "Address": slot.get("address"),
                    #     "Date": session.get("date"),
                    #     "Available": session.get("available_capacity"),
                    #     "Vaccine Type": session.get("vaccine"),
                    #     "Payment Type": slot.get("fee_type"),
                    #     "Time slots": session.get("slots"),
                    # }
                    booking_details = f"VACCINE AVAILABLE\n{slot.get('district_name')}-{slot.get('state_name')}\n{slot.get('name')},{slot.get('address')}\n{session.get('available_capacity')} shots"
                    master_list.append(booking_details)
    return master_list
