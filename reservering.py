import os
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

email = os.getenv("PARKING_EMAIL")
password = os.getenv("PARKING_PASSWORD")
block = os.getenv("PARKING_BLOCK")
location = os.getenv("PARKING_LOCATION")

login_url = "https://thegrid.parkingportal.app/nl/login/"
reserve_url = "https://thegrid.parkingportal.app/nl/reservations/make/"

target_date = date.today() + timedelta(weeks=1)

with requests.Session() as s:
    # 1. Loginpagina ophalen (cookie + token krijgen)
    r = s.get(login_url)
    r.raise_for_status()

    # Cookie csrftoken wordt nu door requests.Session opgeslagen
    soup = BeautifulSoup(r.text, "html.parser")
    form_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    # 2. Login POST met beide tokens
    payload = {
        "email": email,
        "password": password,
        "csrfmiddlewaretoken": form_token,
    }
    headers = {
        "Referer": login_url
    }
    r2 = s.post(login_url, data=payload, headers=headers)
    r2.raise_for_status()

    # 3. Reservering doen
    params = {
        "reservation_date": target_date.isoformat(),
        "reservation_block_settings": block,
        "location": location,
    }
    r3 = s.get(reserve_url, params=params)
    r3.raise_for_status()

    if "bevestigd" in r3.text.lower():
        print("✅ Reservering gelukt!")
    else:
        print("⚠️ Reservering mogelijk niet gelukt.")
