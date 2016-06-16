import os
import sys
from os.path import join as pathjoin

import yaml

APP_DIR = os.path.dirname(__file__)
PLUGINS_DIR = pathjoin(APP_DIR, 'plugins')


def normpath(*args):
    return os.path.normpath(pathjoin(*args))


def get_regylar(key):
    with open(normpath(APP_DIR, 'config/regular.yaml'), 'r') as f:
        data = yaml.load(f)
    assert isinstance(key, object)
    return data[key]


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
