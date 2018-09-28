import requests, json, datetime
from time import sleep
import config as cfg
import urllib


def get_follower_status(username="testuser", channel="jimondaspot"):
    try:
        url = "https://api.twitch.tv/kraken/users/{0}/follows/channels/{1}{2}".format(
            username.lower().lstrip("@"), channel,
            "?client_id=" + "zsrmikty0jlfbypr5ia8afuv8ur3ib"
        )
        resp = requests.get(url=url)
        data = json.loads(resp.content)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                  "Sep", "Oct", "Nov", "Dec"]
        suffixes = ["st", "nd", "rd", "th", ]
        date_split = data["created_at"][:10].split("-")
        year = date_split[0]
        month = months[int(date_split[1]) - 1]
        day = date_split[2]
        follower_since = "{} {}, {}".format(month, day, year)
        return "{} has been following {} since {}.".format(username, channel, follower_since)
    except:
        return "{} doesn't follow {}.".format(username, channel)

def threadGlobalMSG(irc):
    while True and streamStatus(cfg.CHAN):
        irc.sendMessage(cfg.CHAN,"You earn 10 Smugs every 1 minute here. Check your Smugs by typing !smugs.")
        sleep(1500)

def threadOfflineMSG(irc):
    while True:
        if streamStatus(cfg.CHAN):
            sleep(5)
        else:
            irc.sendMessage(cfg.CHAN, "Stream has gone offline. No longer collecting points. Have a nice day!")
            break

def getChannelInfo(channel):
    channel_id = getStreamID(channel)
    url = "https://api.twitch.tv/kraken/channels/" + \
          channel_id
    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "zsrmikty0jlfbypr5ia8afuv8ur3ib"}
    data = requests.get(url, headers=headers)
    data1 = data.json()
    return data1

def getStreamInfo(channel):
    channel_id = getStreamID(channel)
    url = "https://api.twitch.tv/kraken/channels/" + \
          channel_id
    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "zsrmikty0jlfbypr5ia8afuv8ur3ib"}
    data = requests.get(url, headers=headers)
    data1 = data.json()
    return data1

def getStreamID(channel):
    url = "https://api.twitch.tv/kraken/users?login=jimondaspot"
    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "zsrmikty0jlfbypr5ia8afuv8ur3ib"}
    data = requests.get(url, headers=headers)
    data1 = data.json()
    return data1['users'][0]["_id"]

def streamStatus(channel):
    channel_id = getStreamID(channel)
    url = "https://api.twitch.tv/kraken/streams/" + \
          channel_id
    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "zsrmikty0jlfbypr5ia8afuv8ur3ib"}
    data = requests.get(url, headers=headers)
    uptime_data = json.loads(data.content)
    if uptime_data["stream"] is None:
        return False
    else:
        return True

def get_stream_uptime(channel):
    format1 = "%Y-%m-%d %H:%M:%S"
    uptime_data = getStreamInfo(channel)
    if uptime_data["stream"] is not None:
        start_time = str(uptime_data['stream'].get('created_at')).replace(
            "T", " ").replace("Z", "")
        stripped_start_time = datetime.datetime.strptime(start_time, format1)
        time_delta = (datetime.datetime.utcnow() - stripped_start_time)
        return str(time_delta).split(".")[0]
    else:
        return None

def threadFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/jimondaspot/chatters"
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            response = urllib.request.urlopen(req).read()
            cfg.oplist.clear()
            data = json.loads(response)
            for p in data["chatters"]["viewers"]:
                cfg.userList[p] = "viewer"
            for p in data["chatters"]["moderators"]:
                cfg.oplist[p] = "mod"
                cfg.userList[p] = "mod"
            for p in data["chatters"]["global_mods"]:
                cfg.oplist[p] = "global_mod"
                cfg.userlist[p] = "global_mod"
            for p in data["chatters"]["admins"]:
                cfg.oplist[p] = "admin"
                cfg.userList[p] = "admin"
            for p in data["chatters"]["staff"]:
                cfg.oplist[p] = "staff"
                cfg.userList[p] = "staff"
        except:
            'do nothing'
        sleep(5)

