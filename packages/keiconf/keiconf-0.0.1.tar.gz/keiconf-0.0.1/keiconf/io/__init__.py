from appdirs import user_config_dir
from pathlib import Path

def config_path(appname: str = None, author: str = None) -> Path:
    '''
    Given an appname and author, returns a viable path/to/appname.json
    '''
    return Path(f"{user_config_dir(appname, author)}/{appname}.json")

    