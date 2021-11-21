import json
from os import path

dir_path = path.dirname(__file__)
constants_path = path.abspath(path.join(dir_path, "constants.json"))
with open(constants_path) as f:
    CONSTANTS = json.load(f)