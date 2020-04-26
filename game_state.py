import log
from files import save, load

level_info_path = "stats"
level_info_file = "level.info"


def save_level_info(level_info):
    save(level_info, level_info_path, level_info_file)


def load_level_info(default):
    try:
        return load(level_info_path, level_info_file)
    except:
        log.warn("Couldn't load level file, returning default level {}".format(default))
        return {"level": default}
