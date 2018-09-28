from irc import IRC
import config
from threading import Thread
import command_functions as cmd
from commands_list import commands
import twitch, _thread, smugs, config

class Bot(object):
    def __init__(self):
        self.IRC = IRC()
        cmd.loadCusCommands()
        _thread.start_new_thread(twitch.threadFillOpList, ())
        smugs.initSmugs()
        _thread.start_new_thread(twitch.threadOfflineMSG, (self.IRC,))
        _thread.start_new_thread(twitch.threadGlobalMSG, (self.IRC,))
        _thread.start_new_thread(smugs.threadCalcPoints, ())
        print(config.userList)
        self.run()




    def handleMsg(self, username, channel, message):
        if message[0] == "!":
            message = message.lower()
            tempCommand = message.split()[0][1:]
            print(tempCommand)
            if tempCommand in config.cusCommands:
                response = cmd.findCusCommand(tempCommand)
                self.IRC.sendMessage(channel, response)
            elif cmd.is_valid_command(tempCommand):
                if cmd.check_has_correct_args(message, tempCommand):
                    if cmd.get_return(tempCommand) == "command":

                        args = message.split()
                        del args[0]
                        print("args" + str(args))
                        self.IRC.sendMessage(channel, cmd.pass_to_function(tempCommand, args, username = username, channel = channel, bot = self))
                    else:
                        self.IRC.sendMessage(channel, commands[tempCommand]["return"])
            else:
                self.IRC.sendMessage(channel, "Command does not exist.")




    def run(self):

        def receive_data():
            while True:
                try:
                    data = self.IRC.nextMessage()
                    print(data)

                    message = self.IRC.check_for_message(data)

                    if not message:
                        continue
                    if message:
                        message_dict = self.IRC.get_message(data)

                        channel = message_dict.get("channel")
                        message = message_dict.get("message")
                        username = message_dict.get("username")
                        Thread(target=self.handleMsg, args=(
                                username, channel, message)).start()

                except Exception as error:
                    print(error)

        Thread(target=receive_data(), args=("chat",)).start()


bot_instance = Bot()



