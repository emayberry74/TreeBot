import config as cfg
import json
import twitch, time
from Player import Player

def savePoints(username):
    with open("points.json") as data_file:
        data = json.load(data_file)
    for i in data["Users"]:
        if username in i["Username"]:
            if cfg.chatters.get(username).points < 0 or username.lower() is cfg.CHAN:
                cfg.chatters.get(username).points = 0
                i["Current Points"] = 0
            else:
                i["Current Points"] = cfg.chatters.get(username).points
    with open('points.json', 'w') as f:
        f.write(json.dumps(data))

def initSmugs():
    with open("points.json") as data_file:
        data = json.load(data_file)
    for i in data["Users"]:
        temp = Player(i["Username"],i["Current Points"])
        cfg.chatters[temp.username] = temp

def threadCalcPoints():
    with open("points.json") as data_file:
        data = json.load(data_file)
    while True:
        if twitch.streamStatus(cfg.CHAN):
            for p in cfg.userList:
                if p in cfg.chatters:
                    cfg.chatters.get(p).points = cfg.chatters.get(p).points + 10
                    for i in data["Users"]:
                        if p in i["Username"]:
                            i["Current Points"] = cfg.chatters.get(p).points
                    with open('points.json', 'w') as f:
                        f.write(json.dumps(data))
                else:
                    temp = Player(p, 0)
                    cfg.chatters[p] = temp
                    chatter_dict = {"Username": temp.username, "Current Points": temp.points}

                    data["Users"].insert(len(data["Users"]), chatter_dict)
                    with open('points.json', 'w') as f:
                        json.dump(data, f)
        time.sleep(60)


def getSmugs(username):
    if username in cfg.chatters:
        return str(cfg.chatters.get(username).points)
    else:
        return False


def giveSmugs(username, smugs):
    if username in cfg.chatters:
        cfg.chatters.get(username).points = cfg.chatters.get(username).points + int(smugs)
        savePoints(username)
        return True
    else:
        return False


def giveAllSmugs(smugs):
    for username in cfg.chatters:
        cfg.chatters.get(username).points = cfg.chatters.get(username).points + int(smugs)
        savePoints(username)
