import json


def store_data(disctrict_id):
    print(disctrict_id)
    with open(
        "/Users/arpitkjain/Desktop/Data/POC/CoVIDVaccineTracker/cowin_bot/data/check_status.json",
        "r",
    ) as f:
        data = json.load(f)
        f.close()
    dist_list = data["district_list"]
    set_of_dist = set(dist_list)
    set_of_dist.add(disctrict_id)
    data["district_list"] = list(set_of_dist)
    with open(
        "/Users/arpitkjain/Desktop/Data/POC/CoVIDVaccineTracker/cowin_bot/data/check_status.json",
        "w",
    ) as f:
        json.dump(data, f)
        f.close()
