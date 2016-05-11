import sys
import logging
import asyncio

__alias__ = 'mac 全局快捷键'
__version__ = '0.0.1'
__desc__ = 'mac 全局快捷键'


def enable(app):
    logger = logging.getLogger(__name__)
    if sys.platform == 'darwin':
        from .mac import run
        logger.info('load mac hotkey plugin')

        app_event_loop = asyncio.get_event_loop()
        app_event_loop.create_task(run(app))


def disable(app):
    logger = logging.getLogger(__name__)
    logger.info('the developer is so stupid, cant disable this plugin')
