import os
import json


class Config:
    def __init__(self, path: str, auto_save=False):
        
        # PROPERTIES
        self.path = path
        self.auto_save = auto_save

        # CONFIGURATION
        self.config = self.get()

        # BINDINGS
        self.bindings = dict()
    
    def get(self, key: str='', default: object=None) -> object|dict:
        """Returns the dict from JSON file"""
        if not os.path.isfile(self.path):
            self.config = dict()
            return self.config
        
        with open(self.path, 'r') as f: self.config = json.load(f)
        if key: return self.config.get(key, default)
        return self.config
    
    def update(self, key: object, value: object) -> dict:
        """Updates the configuration values"""
        self.config[key] = value
        if key in self.bindings: self.bindings[key](value)
        if self.auto_save: self.save()
    
    def save(self) -> None:
        """Writes the dict on file"""
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def bind(self, variable: str, function: object) -> None:
        """Adds a function to be called when a value is updated"""
        self.bindings[variable] = function