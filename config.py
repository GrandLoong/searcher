import os
import sys
from os.path import join as pathjoin

import yaml

APP_DIR = os.path.dirname(__file__)
PLUGINS_DIR = pathjoin(APP_DIR, 'plugins')


def normpath(*args):
    # type: (object) -> object
    return os.path.normpath(pathjoin(*args))


def get_regexp(key):
    try:
        with open(normpath(APP_DIR, 'config/site.yaml'), 'r') as f:
            data = yaml.load(f)
        config_vars = key.split("/")
        value = data
        for var in config_vars:
            value = value[var]
        return value
    except:
        pass

def get_local_profile_dir():
    profile = "USERPROFILE"
    if sys.platform != "win32":
        profile = "HOME"
    homedir = os.getenv(profile)
    desktop_profile_dir = pathjoin(homedir, '.searcher')
    desktop_profile_dir = os.path.normpath(desktop_profile_dir)
    if not os.path.exists(desktop_profile_dir):
        os.mkdir(desktop_profile_dir)
    return desktop_profile_dir


def add_icon(icon_name):
    return pathjoin(APP_DIR, 'resources', icon_name)
