import requests,json
from pprint import pprint

def streamStatus():
    url = "https://api.twitch.tv/kraken/streams/52743433"
    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "zsrmikty0jlfbypr5ia8afuv8ur3ib"}
    data = requests.get(url, headers=headers)
    uptime_data = json.loads(data.content)
    print(uptime_data)
    if uptime_data["stream"] is None:
        return False
    else:
        return True

streamStatus()