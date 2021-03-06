import requests
import urllib
import json
import datetime

class TimeError(Exception):
    pass

def validate_date(date_in):
    try:
        datetime.datetime.strptime(date_in, '%Y-%m-%d')
        return True
    except ValueError:
        return False



def station(addr, station_code):
    headers = {
        "User-Agent": "Trein.app website backend/1.0"
    }
    station_code_esc = urllib.quote(station_code, safe='')

    r = requests.get(addr + "/v2/station/" + station_code_esc, headers=headers)
    response = json.loads(r.text)
    
    if response['result'] != "OK":
        return False
    
    return response['vertrektijden']
    
def train(addr, day, service_number, station = False):
    headers = {
        "User-Agent": "Trein.app website backend/1.0"
    }

    if validate_date(day) is False:
        raise TimeError("Date input is incorrect")

    day_esc = urllib.quote(day, safe='')
    service_number_esc = urllib.quote(service_number, safe='')
    if station is False:
        requestaddr = addr + "/v2/trein/" + service_number_esc + "/" + day_esc
    else:
        requestaddr = addr + "/v2/trein/" + service_number_esc + "/" + day_esc + "/" + station 
    r = requests.get(requestaddr, headers=headers)
    try:
        response = json.loads(r.text)
    except ValueError:
        return False
    
    if response['result'] != "OK":
        return False
    
    return response['trein']
