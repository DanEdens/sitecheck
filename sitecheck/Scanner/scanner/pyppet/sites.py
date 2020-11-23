"""
    Shared functions for Scanner.pyppet module

    Currently Supported Sites:
    Amp - <project.name>.geo-instruments.com/index.php
    Quickview - https://quickview.geo-instruments.com/login.php
    Truelook (Dev branch) - https://app.truelook.com/<project specific>
"""
import logging
import os
import platform
import pyppeteer.errors
from pyppeteer import launch

from sitecheck.Scanner.scanner import options
from . import text
from . import utlis


logger = logging.getLogger('chrome/log')
log = logging.getLogger('log')


async def make_browser(self):
    """
    Creates a new Browser context

    Returns: browser Object

    """
    system = platform.system()
    if options.Test:
        log.info('Test passed')
        return

    if system == "Linux":
        if self.project.site == 'amp':
            utlis.post('chrome/headless', os.environ['Headless'])
            utlis.post('chrome/site', 'Amp')
            utlis.post('chrome/os', 'Linux')
            self.browser = await launch(
                    executablePath='/usr/bin/chromium-browser',
                    headless=os.environ['Headless'],
                    ignoreHTTPSErrors=True,
                    autoClose=False,
                    args=options.chrome_args
                    )
        elif self.project.site == 'qv':
            utlis.post('chrome/headless', 'False')
            utlis.post('chrome/site', 'QV')
            utlis.post('chrome/os', 'Linux')
            self.browser = await launch(
                    executablePath='/usr/bin/chromium-browser',
                    headless=False,
                    ignoreHTTPSErrors=True,
                    autoClose=False,
                    args=options.chrome_args
                    )
    elif system == "Windows":
        if self.project.site == 'amp':
            utlis.post('chrome/headless', os.environ['Headless'])
            utlis.post('chrome/site', 'Amp')
            utlis.post('chrome/os', 'Windows')
            self.browser = await launch(
                    headless=os.environ['Headless'],
                    ignoreHTTPSErrors=True,
                    autoClose=False,
                    args=options.chrome_args
                    )
        elif self.project.site == 'qv':
            utlis.post('chrome/headless', 'False')
            utlis.post('chrome/site', 'QV')
            utlis.post('chrome/os', 'Windows')
            self.browser = await launch(
                    headless=False,
                    ignoreHTTPSErrors=True,
                    autoClose=False,
                    args=options.chrome_args
                    )
    return self


async def Login(self):
    """
    Handles AMP and QV Authentication.

    :rtype: None
    """
    await self.page.goto(self.url)
    await utlis.wait_count(self, 2)
    for x in [text.Amp_text, text.Qv_text]:
        try:
            await self.page.type(x.logincss, x.username)
            await self.page.type(x.pwcss, x.password)
            await self.page.click(x.loginbutton)
        except (pyppeteer.errors.PageError, pyppeteer.errors.NetworkError):
            pass
    await self.page.waitFor(200)


async def scan_plan_view(parent, platform):
    """
    Iterate through Array of possible Sensor selectors on current planview.

    Absolute selector:
        'body > div:nth-child('(3:4)') > div:nth-child('(0:300)') > a:nth-child(1)'
    Relative selector:
        'body >' + amp.csspath + type_of_sensor_box + ') ' + csspath + self.target_child + amp.title

    :param parent: <projecthandler.Project_runner object at ** >
    :param platform: <class 'pyppet.sites.Amp_Webpage'>

    """
    for target_child in range(0, 300):
        os.environ['TARGET_CHILD'] = str(target_child)
        await platform.get_last_update(parent)
