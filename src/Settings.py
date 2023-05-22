
import configparser

class Settings:

    settings = False

    def __init__(self):
        self.settings = configparser.ConfigParser()
        self.settings.read('settings.ini')


    def get(self, section, name):
        value = self.settings[section][name]
        return value


settings = Settings()
