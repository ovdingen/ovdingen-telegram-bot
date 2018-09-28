import requests
import json
import urllib

def get_station(code, addr):
    headers = {
        "User-Agent": "Spoor.app Telegram app/1.0"
    }
    station_code_esc = urllib.quote(code, safe='')

    r = requests.get(addr + "/station/" + station_code_esc, headers=headers)
    response = json.loads(r.text)
    
    if response['status'] != "OK":
        return False
    
    return response['station']
