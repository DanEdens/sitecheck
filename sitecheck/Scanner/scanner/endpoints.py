"""
    Geo-Instruments
    Sitecheck Scanner
    Endpoints module for Scanner

"""
import logging
logger = logging.getLogger('log')


class parse:

    def __init__(self, userdata, message):
        self.userdata = userdata
        self.message = message
        self.payload = message.payload

    def filter_messages(self):
        if self.payload == 'test':
            logger.info('Test success')
