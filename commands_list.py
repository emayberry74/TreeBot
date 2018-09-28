commands = {
    'test': {
        'argc': 0,
        'op': False,
        'return': 'This is a test!',
        'usage': '!test'
    },

    'currenttime': {
        'argc': 0,
        'op': False,
        'return': 'command',
        'usage': '!currenttime'
    },

    'weather': {
        'argc': 2,
        'op': False,
        'return': 'command',
        'usage': '!weather <city> <state>'
    },

    'addcommand': {
        'argc': "optional",
        'op': False,
        'return': 'command',
        'usage': '!addcommand <command name> <what the command should return>'
    },

    'joinchannel': {
        'argc': 1,
        'op': True,
        'return': 'command',
        'usage': '!joinchannel <name of channel>'
    },

    'smugs': {
        'argc': "optional",
        'op': False,
        'return': 'command',
        'usage': '!smugs or !smugs <username>'
    },

    'help': {
        'argc': "optional",
        'op': False,
        'return': 'command',
        'usage': '!help or !help <command name>'
    },

    'commands': {
        'argc': 0,
        'op': False,
        'return': 'command',
        'usage': '!commands'
    },

    'joinpls': {
        'argc': 1,
        'op': False,
        'return': 'command',
        'usage': '!join <channel name>'
    }
}
