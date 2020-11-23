"""
    Amp navigation functions for Scanner.pyppet module
"""
import logging
import os

logger = logging.getLogger('chrome')
amp = logging.getLogger('chrome')
from sitecheck.Scanner.scanner import data
from sitecheck.Scanner.scanner import options
from . import sites
from . import utlis
from .text import Amp_text


class Amp_Webpage:
    """
    Operator pool for Amp.
    """

    async def goto_plan_view(self):
        """
        Loop through the planviews set in project.planarray

        :rtype: None

        """
        views = self.project.planarray.split(",")

        for view in views:
            logger.debug(f'Navigating to url: '
                         f'{self.url + Amp_text.planview + view}  ')
            await self.page.goto(self.url + Amp_text.planview + view)
            logger.debug(f'Scanning Planview: {view} out of {views}')
            await sites.scan_plan_view(self, Amp_Webpage)

    async def get_last_update(self):
        """
        Loop through possible sensors and gather IDs and recent timestamp.
        :rtype: None
        """
        for _sensor_box in ['3', '4']:
            _name: str = str(
                f"body > div:nth-child({_sensor_box}) "
                f"> div:nth-child({os.environ['TARGET_CHILD']}) "
                f"> a:nth-child(1)"
                )
            name = await self.page.J(_name)

            _data: str = str(
                f"body > div:nth-child({_sensor_box}) "
                f"> div:nth-child({os.environ['TARGET_CHILD']}) "
                f"> a:nth-child(3)"
                )
            link = await self.page.J(_data)

            if name is None:
                pass
            else:
                # Retrieve sensor's Data from Amp

                scan = self.page.evaluate
                _sensor = await scan('(name) => name.textContent', name)
                _date = await scan('(link) => link.title', link)
                await utlis.screenshot(self, _sensor, _name)
                await utlis.detach(self, _sensor)

                # Get Sensor Value. Adds sensor value to output
                if options.Getvalue:
                    _value = await scan('(link) => link.textContent', link)
                    logger.info(f' === Current value: {_value}')

                # Send gathered data to be sorted
                await data.watchdog_handler(
                    utlis.check_date(_date),
                    self.project.name,
                    _sensor,
                    _date
                    )
