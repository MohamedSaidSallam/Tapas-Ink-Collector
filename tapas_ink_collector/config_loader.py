import json

config = {}


def loadConfig():
    global config
    with open('config.json', 'r') as configFile:
        config = json.load(configFile)
