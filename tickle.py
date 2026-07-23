import requests,time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


BASE_URL = "https://localhost:5000/v1/api"

while True:
    request_url = f"{BASE_URL}/tickle"
    json_content = {}
    requests.post(url=request_url, json=json_content,verify=False)
    print("Tickle sent to IBKR API")
    time.sleep(60)