from constant import CACHE_SIZE

CONFIG_DICT = dict({CACHE_SIZE: 128})


def get_config(key):
    global CONFIG_DICT
    return CONFIG_DICT[key]


def set_config(key, value):
    global CONFIG_DICT
    CONFIG_DICT[key] = value