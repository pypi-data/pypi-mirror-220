import yaml
import pathlib
import logging
import sys

from . import models

logger = logging.getLogger(__name__)

try:
    import np_config
except ImportError:
    logger.error("Error importing np_config.", exc_info=True)


def from_file(config_file: pathlib.Path) -> models.RegimenUpdateRecipie:
    return models.RegimenUpdateRecipie.from_dict(
        yaml.safe_load(config_file.read_text())
    )


def from_np_config(np_config_name: str) -> models.RegimenUpdateRecipie:
    try:
        resolved = np_config.from_zk(np_config_name)
        return models.RegimenUpdateRecipie.from_dict(resolved)
    except Exception as e:
        logger.error("Error loading np_config. np_config_name=%s" % np_config_name)

