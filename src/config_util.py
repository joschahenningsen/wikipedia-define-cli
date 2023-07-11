import configparser
import os.path
from pathlib import Path

import appdirs

APP_NAME = 'wikipedia-define-cli'

CONFIG_DIR = appdirs.user_config_dir(APP_NAME)
CONFIG_FILE_NAME = 'config'
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)

SECTION_DEFAULT = 'default'
CONFIG_DEFAULT_LANG = 'lang'

# create config directory if not already existing
if not Path(CONFIG_FILE_PATH).exists():
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)

# load existing config
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

# add section if not existing
if not config.has_section(SECTION_DEFAULT):
    config.add_section(SECTION_DEFAULT)


def save_config():
    with open(CONFIG_FILE_PATH, 'w+') as config_file:
        config.write(config_file)


def setup_default_lang():
    config.set(SECTION_DEFAULT, CONFIG_DEFAULT_LANG, 'en')
    save_config()


def get_default_lang():
    if not config.has_option(SECTION_DEFAULT, CONFIG_DEFAULT_LANG):
        setup_default_lang()
    return config.get(SECTION_DEFAULT, CONFIG_DEFAULT_LANG)
