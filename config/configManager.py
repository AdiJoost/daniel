import json
import copy
from pathlib import Path
from config.rootPath import getRootPath
from config.configFiles import ConfigFiles

CONFIG_FOLDER = "config"


application_config = {}


with open(getRootPath().joinpath(CONFIG_FOLDER, "applicationConfig/applicationConfig.json"), "r") as file:
    application_config = json.load(file)



def loadConfig():
    return "Hello"

def getConfig(name: str, config: ConfigFiles=ConfigFiles.APPLICATION_CONFIG) -> any:
    if config == ConfigFiles.APPLICATION_CONFIG:
        return _getConfig(name, application_config)

def _getConfig(name:str, config: dict) -> any:
    return _returnCopy(config.get(name))

def _returnCopy(object) -> any:
    if object == None:
        return None
    if isinstance(object, list) or isinstance(object, dict):
        return copy.deepcopy(object)
    return object
    