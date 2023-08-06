from netbox_network_importer import __appname__

import os
import sys
import appdirs
import yaml

import logging
from loguru import logger

os.environ["XDG_CONFIG_DIRS"] = "/etc"
CONFIG_DIRS = (
    appdirs.user_config_dir(__appname__),
    appdirs.site_config_dir(__appname__),
)
CONFIG_FILENAME = "config.yml"


def get_config():
    """
    Get config file and load it with yaml
    :returns: loaded config in yaml, as a dict object
    """
    if getattr(get_config, "cache", None):
        return get_config.cache

    if os.environ.get("CONFIG_FOLDER_PATH"):
        config_path = os.path.join(
            os.environ["CONFIG_FOLDER_PATH"], CONFIG_FILENAME)
    else:
        for d in CONFIG_DIRS:
            config_path = os.path.join(d, CONFIG_FILENAME)
            if os.path.isfile(config_path):
                break
    try:
        with open(config_path, "r") as config_file:
            conf = yaml.safe_load(config_file)
            get_config.cache = conf
            return conf
    except FileNotFoundError as e:
        logger.debug(e)
        if os.environ.get("CONFIG_FOLDER_PATH"):
            logger.error(
                "Configuration file not found at {}.".format(
                    os.environ["CONFIG_FOLDER_PATH"]
                )
            )
            exit(0)
        else:
            logger.error(
                "No configuration file can be found. Please create a "
                "config.yml in one of these directories:\n"
                "{}".format(", ".join(CONFIG_DIRS))
            )
            exit(0)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger(file=True, stderr=True):
    try:
        log_level = get_config()['config'].get('LOG_LEVEL', "INFO")
    except:
        log_level = "INFO"

    logger.remove()

    try:
        if stderr:
            logger.add(sys.stderr, level=log_level)

        if file:
            log_path = get_config().get('config', {}).get('LOG_DIR', None)

            if log_path and os.path.isdir(log_path):
                logger.add(os.path.join(log_path, "output.log"),
                        rotation="5 MB", level=log_level)
            else:
                logger.remove()
                logger.add(sys.stderr)
                logger.error(
                    f"Logging directory {log_path} does not exists. Set a proper 'LOG_DIR' var in configuration file")
                exit(0)

        # bypass standard logging into loguru
        logging.basicConfig(handlers=[InterceptHandler()], level=0)        
    except Exception as e:
        logger.remove()
        logger.add(sys.stderr)
        logger.exception("Something went wrong", e)
        exit(0)