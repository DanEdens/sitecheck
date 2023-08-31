"""
    Utilities Package for Pyppet
"""
import logging
import os
import sys

import paho.mqtt.client as paho
from dateutil.parser import parse

logger = logging.getLogger('chrome')
client = paho.Client("qv", clean_session=True)
client.connect("3.134.3.199", 1884)


def check_date(time) -> str:
    """
    Check time since the current time
    :param time:
    :return: Diffrence in seconds
    :rtype: int
    """
    now = parse(os.environ['Nowdate'])
    return int((now - parse(time)).total_seconds())


async def wait_type(page, selector, txt):
    """
    :param: page
    :param: selector
    :param: txt

    Wait for a selector to load than type supplied text.

    :returns: page
        This is in case the pages response to text changes the browser context.

    """
    await page.waitForSelector(selector)
    await page.type(selector, txt)
    return page


async def click(page, selector):
    """
    :param: page
    :param: selector

    Wait for a selector to load, than click on it.

    :returns: page
        This is in case click navigation changes the browser context.
    """
    await page.waitForSelector(selector),
    await page.click(selector)
    return page


async def wait_hover(page, selector):
    """
    :param: page
    :param: selector

    Wait for a selector to load, than hover over it.

    :returns: page
        This is in case page response changes the browser context.
    """
    await page.waitForSelector(selector),
    await page.hover(selector)
    return page


async def detach(self, sensor):
    """
    End Process after detaching from browser
    :param sensor:  
    :param self:  
    """
    if sensor == os.environ['DETACH']:
        logger.debug(f'Detached from Browser. Endpoint: {self.browser.wsEndpoint}')
        post(f'chrome/bep/{sensor}', f'{self.browser.wsEndpoint}')
        await self.browser.disconnect()
        sys.exit()
    else:
        return


async def screenshot(self, sensor='_', name_selector='_'):
    """

    :param self: 
    :param sensor: 
    :param name_selector: 
    :return: 
    """
    if sensor in os.environ['imagelist']:
        _date = os.environ['Nowdate']
        project_images = f"{os.environ['ROOT_DIR']}\\Screenshots\\{self.project.name}\\"
        _tmp = f'{project_images}{sensor}_{_date}.png'
        path = _tmp.replace(' ', '_')
        await wait_hover(self.page, name_selector)
        await self.page.waitFor(500)
        await self.page.screenshot({'path': path})
        logger.debug(f'Screenshot saved at: {path}')


def disable_timeout_pyppeteer():
    """
        :Pyppeteer upstream depricates need for this:
        Disables built-in max browser interation Timeout

        :returns: original_method(*args, **kwargs)
    """
    import pyppeteer.connection

    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


async def wait_count(self, count):
    """
    Wait for {count}, While printing seconds remanining
    :param self: Page context
    :param count: NUmber of seconds to wait
    :return: none
    """
    while count > 0:
        wait_time = str(count)
        logger.debug(f"Waiting {wait_time} seconds for Page load..")
        count -= 1
        await self.page.waitFor(1000)
    return


def post(topic, payload, retain=False):
    """
    Post results to MQTT broker for processing
    :param retain: 
    :param topic: Project name
    :param payload: Sensor Data
    """
    topic = str(f'Scanner/{topic}')
    payload = str(payload)
    try:
        client.publish(topic, payload, retain)
        # logger.debug(payload)
    except ValueError:
        logger.info(
            f"pub Failed because of wildcard: {str(topic)}=:={str(payload)}")
        logger.info(f"Attempting fix...")
        try:
            tame_t = topic.replace("+", "_")
            tame_topic = tame_t.replace("#", "_")
            tame_p = payload.replace("+", "_")
            tame_payload = tame_p.replace("#", "_")
            logger.info("Fix successful, Sending data...")
            client.publish(str(tame_topic), str(tame_payload), retain)
            # logger.debug(payload)
        except Exception as error:
            logger.info(f"Fix Failed. Bug report sent.")
            client.publish("Scanner/error", str(error), qos=1, retain=True)
