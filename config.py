'''Reading in config data'''

import json
from dataclasses import dataclass

# TODO
# Add docstrings

@dataclass
class Config:
    database_location: str

def load_config(path: str) -> Config:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Config(**data)