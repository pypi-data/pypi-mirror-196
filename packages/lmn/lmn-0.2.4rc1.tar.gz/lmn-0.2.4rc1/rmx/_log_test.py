#!/usr/bin/env python3
from rmx import logger

if __name__ == '__main__':
    from logging import DEBUG
    logger.setLevel(DEBUG)
    logger.debug('This is DEBUG')
    logger.info('This is INFO')
    logger.warning('This is WARNING')
    logger.error('This is ERROR')
    logger.critical('This is CRITICAL')
