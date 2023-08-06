import os
import time
from SherLocking.config import Config


class File:
    def __init__(self, path: str):
        
        # PROPERTIES
        self.path = path
    
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        print(type_, value, traceback)
    
    def read(self) -> None:
        """Reads the content of the file"""
        with open(self.path, 'r') as f:
            return f.read()
    
    def write(self, text: str, mode: str='w') -> None:
        """Write into the file"""
        with open(self.path, mode) as f:
            f.write(text)


class HiddenFile(File):
    def __init__(self, path: str, delay: int=1):
        super().__init__(path)

        # PROPERTIES
        self.path = path
        self.delay = delay
    
    def hide_file(self) -> bool:
        """Makes the file no visible"""
        if not os.path.isfile(self.path): return False
        os.system(f'attrib +h {self.path}')
        time.sleep(self.delay)
        return True

    def show_file(self) -> bool:
        """Makes the file visible"""
        if not os.path.isfile(self.path): return False
        os.system(f'attrib -h {self.path}')
        time.sleep(self.delay)
        return True


class HiddenConfig(HiddenFile, Config):
    def __init__(self, path: str, auto_save=True):
        HiddenFile.__init__(self, path)
        Config.__init__(self, path, auto_save=auto_save)
    
    def get(self, key: str='') -> dict:
        """Returns the content of the config"""
        self.show_file()
        config = super().get(key)
        self.hide_file()
        return config

    def save(self) -> None:
        """Saves the config"""
        self.show_file()
        super().save()
        self.hide_file()
        