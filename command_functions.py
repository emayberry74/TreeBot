from commands_list import commands
import importlib
import json
import config as cfg

def is_valid_command(command):
	if command in commands:
		return True

def get_return(command):
	return commands[command]['return']

def get_argc(command):
    return commands[command]['argc']

def check_has_correct_args(message, command):
    message = message.split(' ')

    if commands[command]['argc'] is 'optional':
        return True
    if 'argc' not in commands[command]:
        return True
    if len(message) - 1 == commands[command]['argc']:
        return True


def addCusCommands(cmd, response):
    with open("commands.json") as data_file:
        commands = json.load(data_file)

    if cmd in cfg.cusCommands:
        removeCusCommands(cmd)

    commands_dict = {"Command": cmd, "Response": response}
    cfg.cusCommands[cmd] = response

    commands["Commands"].insert(len(commands["Commands"]), commands_dict)
    with open('commands.json', 'w') as f:
        json.dump(commands, f)

def loadCusCommands():
    with open("commands.json") as data_file:
        commands = json.load(data_file)
    for i in commands["Commands"]:
        print("test2")
        cfg.cusCommands[i["Command"]] = i["Response"]

def removeCusCommands(cmd):
    with open("commands.json") as data_file:
        commands = json.load(data_file)

    for i in range(len(commands["Commands"])):
        if commands["Commands"][i]['Command'] == cmd:
            del commands["Commands"][i]
            print(12)
            break

    with open('commands.json', 'w') as f:
       json.dump(commands, f)

    if cmd in cfg.cusCommands:
        del cfg.cusCommands[cmd]

def findCusCommand(cmd):
    if cmd in cfg.cusCommands:
        return cfg.cusCommands.get(cmd)
    if cmd.lower() in cfg.cusCommands:
        return cfg.cusCommands.get(cmd)

def pass_to_function(command, *args, **kwargs):
    command = command.replace('!', '')
    print(command)
    module = importlib.import_module('commands.%s' % command)
    print(module)
    print(2)
    function = getattr(module, command)

    if args:
        return function(*args[0], **kwargs)
    else:
        return function(*args[0], **kwargs)