import os
import json
import requests
from langchain.agents import tool
# For demo
API_END_POINT_AIOT = "http://140.127.196.78:4443"

@tool
def light_status(str_obj) -> str:
    """Return the lingt status."""

    url = API_END_POINT_AIOT + "/status"
    response = requests.request("GET", url)
    return json.dumps(response.text)

@tool
def light_on(str_obj) -> str:
    """Turn on the light."""

    url = API_END_POINT_AIOT + "/aiot?status=1"
    response = requests.request("GET", url)
    return json.dumps(response.text)

@tool
def light_off(str_obj) -> str:
    """Turn off the light."""

    url = API_END_POINT_AIOT + "/aiot?status=0"
    response = requests.request("GET", url)
    return json.dumps(response.text)
