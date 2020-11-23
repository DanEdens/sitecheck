"""
    Geo-Instruments
    Sitecheck Scanner

    CLI entry point and function pool
"""
# __name__ = 'Scanner'
# __author__ = "Dan Edens"
# __url__= "https://geodev.geo-instruments.com/DanEdens/Sitecheck_Scanner"


import os
import sys

import paho.mqtt.client as mqtt
from ptpython.repl import embed

from sitecheck.Scanner.scanner import config
from sitecheck.Scanner.scanner import options
from sitecheck.Scanner.scanner import utlis
from sitecheck.Scanner.scanner import endpoints

hostname = os.environ.get('awsip')
port = int(os.environ.get('awsport', '-1'))
client = mqtt.Client("Scanner", clean_session=True)
client.connect(hostname, port)

# Logger streams
logger = utlis.make_logger('log')
config_log = utlis.make_logger('config')
data_log = utlis.make_logger('data')
projecthandler_log = utlis.make_logger('projecthandler')
utlis_log = utlis.make_logger('utlis')
chrome = utlis.make_logger('chrome')
chrome_log = utlis.make_logger('chrome/log')
amp = utlis.make_logger('amp')

projects = config.read_config_file()


async def Scan():
    """
    Invoke to Scan all projects marked with "skip = false" in projects.ini
    """
    from sitecheck.Scanner.scanner import projecthandler

    utlis.post(f'arguments', f"Scan Confirmed >> scanner {sys.argv}")
    utlis.post('ProjectTable',
               f'\n{utlis.projects_table(config.read_config_file())}')
    [await (projecthandler.run_controller(project)) for project in
     projects.sections()]
    logger.info('\nScan completed.')


async def daemon(topic='Scanner/stdin'):
    """Create an MQTT client daemon that listens for commands"""
    client.subscribe(topic)
    client.publish('Scanner/log', f"Daemon activated for topic '{topic}'")
    client.on_message = on_message
    client.loop_forever()


async def on_message(userdata, message):
    client.publish('Scanner/stdout',
                   f"{message.topic}: Received message ""'{str(message.payload)} \n'"
                   f"With userdata: {str(userdata)}")
    endpoints.parse(userdata, message)


def repl():
    """
    Repl mode entry point. 
    Implies debug, check, and headful modes
    """
    projects = config.read_config_file()
    utlis.post('Scanner/repl', f"True", retain=True)
    embed(globals(), locals())
    utlis.post('Scanner/repl', f"False", retain=True)


def edit():
    """
    Edits project config file
    """
    config.edit_project()
    # projects = config.read_config_file()
    # return projects


def enable_all_projects():
    """
    Quick reset of all projects to skip = false
    """
    for each in projects.sections():
        config.edit_config_option(each, 'skip', 'false')


def add(name, views='0', page='qv', skip='false'):
    """
    Add a new project to projects file
    :param name: project shortname 
    :param views: Planviews to scan 0,1,2
    :param page: qv/amp
    :param skip: true/false
    """
    config.edit_config_option(name, 'name', name)
    config.edit_config_option(name, 'planarray', views)
    config.edit_config_option(name, 'site', page)
    config.edit_config_option(name, 'skip', skip)
