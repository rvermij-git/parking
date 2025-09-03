import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://thegrid.parkingportal.app"

email = os.getenv("PARKING_EMAIL")
password = os.getenv("PARKING_PASSWORD")
block = os.getenv("PARKING_BLOCK")
location = os.getenv("PARKING_LOCATION")

login_url = f"{BASE_URL}/nl/login/?next=/nl/reservations/"
reserve_url = f"{BASE_URL}/nl/reservations/make/"

with requests.Session() as s:
    # Stap 1: loginpagina ophalen voor CSRF
    resp = s.get(login_url)
    print("Login page status:", resp.status_code)
    soup = BeautifulSoup(resp.text, "html.parser")
    token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    # Stap 2: login POST
    login_data = {
        "username": email,
        "password": password,
        "csrfmiddlewaretoken": token,
        "next": "/nl/reservations/"
    }
    headers = {"Referer": login_url}
    login_response = s.post(login_url, data=login_data, headers=headers)

    print("Login POST status:", login_response.status_code)
    print("Login response URL:", login_response.url)
    print("Login response preview:", login_response.text[:400])

    # Stap 3: reservering proberen
    params = {
        "reservation_date": "2025-09-05",  # <-- later dynamisch maken!
        "reservation_block_settings": block,
        "location": location,
    }
    reservation_response = s.get(reserve_url, params=params)

    print("Reservation request status:", reservation_response.status_code)
    print("Reservation request URL:", reservation_response.url)
    print("Reservation response preview:", reservation_response.text[:400])

    if "bevestigd" in reservation_response.text.lower():
        print("✅ Reservering lijkt gelukt!")
    else:
        print("⚠️ Reservering mogelijk niet gelukt.")
