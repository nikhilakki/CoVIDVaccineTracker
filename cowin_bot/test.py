import requests
from datetime import datetime

today = datetime.now()
start_date = today.strftime("%d-%m-%Y")


def get(route, params=None):
    url = route
    # print(f"url = {url}, params = {params}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers)
    print(response)
    if response.status_code != 200:
        raise Exception(
            f"Call to {route} failed with {response.status_code} and response {response.text}"
        )
    return response.text


get(
    route="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
    params={"district_id": "390", "date": start_date},
)
