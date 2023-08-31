"""
    Pyppet Module

    TODO: move imports to this location,
    TODO: to allow use as a stand alone module
"""
# __name__ = 'pyppet'
import logging
import os

from . import sites
from . import utlis
from .amp import Amp_Webpage as amp
from .quickview import Qv_Webpage as qv

logger = logging.getLogger('chrome')

os.environ['PREVIOUS_SENSOR'] = ''


async def login(self):
    """ Authenticate user on either Amp or QV """
    await sites.Login(self)
    return


async def amp_runner(self):
    """
    Main Operator of the Amp scanner.

    Creates the new page and gives it a viewport.
    Than handles gathering and output of data for Amp scanner.
    """
    logger.info('Launching Amp..')
    await login(self)
    await amp.goto_plan_view(self)


async def qv_runner(self):
    """
    Main Operator of the QV scanner.

    Handles gathering and output of data for QV scanner.
    """
    logger.info('Launching QV..')
    self.url = 'https://quickview.geo-instruments.com/login.php'
    await login(self)
    await qv.goto_project(self)
    await qv.goto_plan_view(self)


#  Browser functions 
async def launch(self):
    """
    Create Browser Object
    """
    utlis.disable_timeout_pyppeteer()
    await sites.make_browser(self)
    pages = await self.browser.pages()
    self.page = pages[0]
    await self.page.setViewport({"width": 1980, "height": 944})
    return self


async def url(self, _url="https://www.geo-instruments.com/"):
    """ Navigate to given url """
    await self.page.goto(_url)
    await utlis.wait_count(self, 2)

