from .. import hookimpl
from ..errors import CantaloupeError
from ..logger import get_root_logger


@hookimpl(wrapper=True)
def cantaloupe_setup(config, context) -> None:
    logger = get_root_logger(config.get_log_level())
    try:
        yield  # execute other hooks here
    except CantaloupeError as e:
        if config.option.failfast:
            raise e
        logger.error(e)


@hookimpl(wrapper=True)
def cantaloupe_build_workflow(config, context, workflow) -> None:
    logger = get_root_logger(config.get_log_level())
    try:
        yield  # execute other hooks here
    except CantaloupeError as e:
        if config.option.failfast:
            raise e
        logger.error(e)
