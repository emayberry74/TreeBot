import requests
import socket
import re
import config as cfg

class IRC:
    def __init__(self):
        self.s = socket.socket()
        self.connect()
        self.msgBuffer = {}

    def nextMessage(self):
        line = self.s.recv(1024).decode("utf-8")


        if line is not None:
            if line.startswith("PING"):
                self.s.send(line.replace("PING", "PONG") + "\r\n")
            return line

    def check_for_message(self, data):
        if re.match(
                r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$',
                data):
            return True

    def get_message(self, data):
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        username = re.search(r"\w+", data).group(0)
        channel = re.search('(?<=#)\w+', data).group(0)
        message = CHAT_MSG.sub("", data)
        d = dict(username=username, channel=channel, message = message)
        return d


    def connect(self):
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((cfg.HOST, cfg.PORT))
        self.s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
        self.s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
        self.joinChannels(cfg.CHAN)


    def joinChannels(self,channels):
        print("THIS IS THE" + channels)
        self.s.send("JOIN #{}\r\n".format(channels).encode("utf-8"))
        self.sendMessage(channels, "Joined")
        print("Joined " + channels)

    def leaveChannels(self,channels):
        self.s.send("PART #{}\r\n".format(channels).encode("utf-8"))
        print("Left " + channels)

    def sendMessage(self, channel, message):
        self.s.send("PRIVMSG #{} :{}\r\n".format(channel, message).encode(encoding='utf-8'))
        print(message)



