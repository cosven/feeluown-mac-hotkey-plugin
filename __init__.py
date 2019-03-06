import sys
import logging
import asyncio

__alias__ = 'mac 全局快捷键'
__version__ = '2.0'
__desc__ = 'mac 全局快捷键'


def enable(app):
    logger = logging.getLogger(__name__)
    if sys.platform == 'darwin':
        from .mac import run
        run()


def disable(app):
    logger = logging.getLogger(__name__)
    logger.info('the developer is so stupid, cant disable this plugin')
