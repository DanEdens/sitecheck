"""
    Geo-Instruments
    Sitecheck Scanner
    Utilities Package for Scanner

"""
import errno
import logging
import os
from pathlib import Path

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from texttable import Texttable

from . import config
from .config import client
from . import options

logger = logging.getLogger('utlis')

filedate = os.environ.get['filedate']


def make_logger(name) -> object:
    """
    Create the project wide logger.
    Sets Output level from Argument flags and if output should be directed
    to a log file.
    Default location is Onedrive/Scanner
    :param name:
    :return: Logger
    :rtype: Object
    """
    if options.Debug:
        _format: str = '%(asctime)s - %(module)s - %(message)s'
    else:
        _format: str = '%(asctime)s - %(message)s'

    log = logging.getLogger(name)

    if options.Log:
        _log = ensure_exists(
            Path(os.environ['Output']).joinpath(
                f"data//{os.environ['filedate']}//scan_report.log"
                ))
        with open(_log, 'a') as file:
            file.write(
                '\nRun Log for {filedate}\n=============================\n')
        logging.basicConfig(filename=_log, level=None, format=_format)
    else:
        logging.basicConfig(level=None, format=_format)

    if options.Debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    myHandler = MQTTHandler(topic=f'Scanner/{name}')
    log.addHandler(myHandler)
    return log


def remove_file(*args):
    """
    Removes Old copy of **file** is file exists
    :param file: File to be replaced
    :return: none

    """
    for file in args:
        try:
            os.remove(file)
            logger.debug(f'Removing previous copy of {file}.. ')
        except OSError:
            pass


def ensure_exists(path):
    """
    Accepts path to file, than creates the directory path if it does not exist
    :param path:
    :return:
    """
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path


class MQTTHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a MQTT server to a topic.
    """

    def __init__(self,
                 _hostname=config.hostname,
                 topic='Scanner/log',
                 qos=0, retain=False,
                 _port=config.port,
                 client_id='',
                 keepalive=60,
                 will=None,
                 auth=None,
                 tls=None,
                 protocol=mqtt.MQTTv31,
                 transport='tcp'):
        logging.Handler.__init__(self)
        self.topic = topic
        self.qos = qos
        self.retain = retain
        self.hostname = _hostname
        self.port = _port
        self.client_id = client_id
        self.keepalive = keepalive
        self.will = will
        self.auth = auth
        self.tls = tls
        self.protocol = protocol
        self.transport = transport

    def emit(self, record):
        """
        Publish a single formatted logging record to a broker, then disconnect
        cleanly.
        """
        msg = self.format(record)
        publish.single(self.topic, msg, self.qos, self.retain,
                       hostname=self.hostname, port=self.port,
                       client_id=self.client_id,
                       keepalive=self.keepalive,
                       will=self.will, auth=self.auth, tls=self.tls,
                       protocol=self.protocol, transport=self.transport)


def projects_table(projects):
    """

    :param projects:
    """
    table = Texttable()
    table.set_cols_align(["l", "l", "l", "r"])
    table.set_cols_valign(["t", "t", "t", "t"])
    table.header(["Project Name", "Views to scan", "Platform", "Skipping"])
    for project in projects.sections():
        x = config.tuple_from_section_config(project)
        table.add_row([x.name, x.planarray, x.site, x.skip])
    return table.draw()


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
