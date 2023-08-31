"""
    Geo-Instruments
    Sitecheck Scanner
"""
# __name__ = "scanner"
# __author__ = "Dan Edens"
# __url__= "https://github.com/DanEdens/Sitecheck_Scrapper"
# __status__  = "production"

import logging
import os


logger = logging.getLogger('log')
projectstore = os.environ['ROOT_DIR'] + '/projects.ini'
