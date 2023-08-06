import importlib_resources as res
import logging.config
import yaml
import ronds_sdk


def config():
    log_config = res.read_text(ronds_sdk, "logging_config.yml", encoding='utf-8', errors='strict')
    logging.config.dictConfig(yaml.safe_load(log_config))
    print('*' * 20)
    print("logger config inited ~")
