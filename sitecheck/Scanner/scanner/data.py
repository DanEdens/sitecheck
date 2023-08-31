"""
    Geo-Instruments
    Sitecheck Scanner
    Data handler Package for Scanner

"""
import json
import logging
import os
from pathlib import Path

import paho.mqtt.client as mqtt

from . import options
from . import utlis

logger = logging.getLogger('data')

hostname = os.environ.get('awsip')
port = int(os.environ.get('awsport', '-1'))

client = mqtt.Client("qv", clean_session=True)
client.connect(hostname, port)


def check_mode(sensor: object) -> object:
    """
    Pauses run to give observer the chance to look at the information before proceeding.

    :return: Wait for input
    :rtype: object
    """
    return
    if os.environ['Repl']:
        logger.log(f'{sensor} is missing data')
        return input(
            "Pausing run for eval.\nPress Enter to continue...")


class watchdog_handler: 
    """
    Handles sorting sensor watchdog status.

    Timeesamps from last update are sorted into three categories:
    Up-to-date, Behind, Old

    :param diff: Time since last reading
    :type diff: int

    :param project_name: Name of Project
    :type project_name: str

    :param sensor: Sensor ID
    :type sensor: str

    :param last_updated: Formatted Date string
    :type last_updated: str
    """
    def __init__(self, diff, project_name, sensor, last_updated):
        """
        Sensor watchdog sorter
        
        :param diff: 
        :param project_name: 
        :param sensor: 
        :param last_updated: 
        """
        self.diff = diff
        self.project_name = project_name
        self.sensor = sensor
        self.last_updated = last_updated
        
        if self.diff <= options.Watchdog:
            self.updated()
        elif options.Watchdog <= self.diff <= options.Oldperiod:
            self.behind()
        else:
            self.older_issue()
        
    def updated(self):
        data_list = [
            self.project_name,
            self.sensor,
            self.last_updated
            ]
        if options.PrintNew:
            logger.info(data_list)
            store(self.project_name, data_list)
        else:
            logger.debug(data_list)

    def behind(self):
        data_list = [
            self.project_name,
            self.sensor,
            f'Older than {options.args.time} hours'
            f"Time since: {convert(self.diff)}.",
            f"Last update: {self.last_updated}."
            ]
        store(self.project_name, data_list)
        
    def older_issue(self):
        """Sensor is Old. Assumes after a week that this is a known issue."""
        data_list = [
            self.project_name,
            self.sensor,
            'Older than a week',
            convert(self.diff),
            self.last_updated
            ]
        if options.PrintOld:
            store(self.project_name, data_list)
        else:
            logger.debug(data_list)
 

def store(project, data_list):
    """
    Sensor Data storage
    Posts to mqtt as retained message

    :param project:	Project name
    :type project: str

    :param data_list: Sensor Data
    :type data_list: str

    :rtype: None
    """
    if os.environ['SCANNER_OUTPUT_TYPE'] == 'file':
        store_path = Path(f"{os.environ['Output']}"
                          f"//data"
                          f"//{os.environ['filedate']}"
                          f"//{project}.txt")
        utlis.ensure_exists(store_path)
        with open(store_path, 'a') as file:
            if not file.tell():
                file.write('[')
            else:
                file.write(',')
            file.write(json.dumps(data_list))
    elif os.environ['SCANNER_OUTPUT_TYPE'] == 'mqtt':
        utlis.post(project, data_list, retain=True)
    else:
        print(project, data_list)
        
def retrieve(topic):
    client.subscribe(topic)


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)
