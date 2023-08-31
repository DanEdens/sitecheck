#!E:\Python\ python
"""
    Data_check.py
"""
import argparse
import errno
import json
import logging
import os
import sys
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import paho.mqtt.client as paho
import pyodbc

# EDIT OPTIONS #######################################################
# You can override these by passing arguments '--debug --time 12'

watchdog_in_hours: int = 24
staletime_in_hours: int = 336  # 2 weeks
log_to_file: bool = True
debug_mode: bool = False
mqtt_mode: bool = True

# END EDIT OPTIONS ###################################################

# Connect to database
conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};'
                      'Server=localhost;'
                      'Database=QUICKVIEW_DB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

client = paho.Client("qv", clean_session=True)
client.connect("3.134.3.199", 1884)


# Parse runtime Arguments
parser = argparse.ArgumentParser(
        description='data_check script',
        prog='data_check',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
parser.add_argument('-l', '--log', action='store_true', default=log_to_file,
                    help='Log output to file')
parser.add_argument('-d', '--debug', action='store_true', default=debug_mode,
                    help="Output Verbose information for debugging")
parser.add_argument('-m', '--mqtt', action='store_true', default=mqtt_mode,
                    help="Output to mqtt server")
parser.add_argument('-t', '--time', default=watchdog_in_hours, metavar='',
                    type=int, help="Set watchdog time in HR")
parser.add_argument('-s', '--stale', default=staletime_in_hours, metavar='',
                    type=int, help="Set Stale time in HR")
args = parser.parse_args()
WatchdogHR = args.time
StaleHR = args.stale
debug = args.debug
do_log_file = args.log
mqtt = args.mqtt

# Declare static variables
filedate = datetime.utcnow().strftime("%Y-%m-%d")
WatchdogTime = (datetime.now() - timedelta(hours=WatchdogHR))
StaleTime = (datetime.now() - timedelta(hours=StaleHR))
root = os.path.dirname(os.path.abspath(__name__))
store_path = Path(f"{root}//Data//{filedate}.json")


# Utlity functions
def ensure_exists(file):
    """ Creates the directory's above file if it they do not exist """
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def remove_file(*args):
    """ Removes Old copy if file exists """
    for file in args:
        try:
            os.remove(file)
            print(f'Removing previous copy of {file}..')
        except OSError:
            pass


def make_logger() -> object:
    """ Makes the logger """
    _logger = logging.getLogger('log')
    logformat = logging.Formatter("%(message)s")

    if debug:
        _level = 'DEBUG'
    else:
        _level = 'INFO'

    if do_log_file:
        logfile = os.path.join(root, f'runlog\\{filedate}.log')
        ensure_exists(logfile)
        fh = logging.FileHandler(logfile)
        fh.setFormatter(logformat)
        fh.setLevel(level='DEBUG')
        _logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logformat)
    ch.setLevel(level=_level)
    _logger.addHandler(ch)
    _logger.setLevel(level=_level)
    return _logger


def fetch(data: str):
    """
    Bundles execute and fetch
    :param data: str
    :return: iterable object
    """
    cursor.execute(data)
    result = cursor.fetchall()
    return result


def post(topic, payload):
    logger.debug(f"pub: {str(topic)}=:={str(payload)}")
    client.publish(str(topic), str(payload), qos=0, retain=False)


def store(self):
    """
    Output data in json
    Example [11978,SP04,2020-08-11 08:00:00,-1.6457,0.0,0.0]
    """
    ensure_exists(store_path)
    x = {
            "project":     f"{self.name}",
            "date":        f'{self.data[0][1]}',
            "Sensor Name": f"{self.sensor_name}",
            "data":        [
                    {"value_1": f"{self.data[0][2]}"},
                    {"value_2": f"{self.data[0][3]}"},
                    {"value_3": f"{self.data[0][3]}"},
                    ]
            }
    with open(store_path, 'a') as file:
        if not file.tell():
            file.write('[')
        else:
            file.write(',')
        if mqtt:
            x = f"{self.sensor_name} Last updated: {self.data[0][1]}"
            post(f"Scanner/lists/{self.name}.txt", x)
        else:
            file.write(json.dumps(x))


def check_data(data):
    """Check if data exists """
    if len(data) != 0:
        pass
    else:
        logger.warn('Data not found')


# Retrieve and filter data
# noinspection PyAttributeOutsideInit
class each_project:
    """
    Create project object and run data check
    :param project: QV project name
    """

    def __init__(self, project):
        self.project = project
        self.project_id = (project[0])
        self.name = (project[1])
        self.data = fetch(
                f"SELECT [ID],[NAME],[PROJECT_ID],[ACTIVE] FROM "
                f"[QUICKVIEW_DB].[dbo].[VIEWS] WHERE Project_ID = "
                f"'{project[0]}' and ACTIVE = 'TRUE'"
                )

    def __enter__(self):
        for x in self:
            logging.debug(x)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('\nEnd Run')

    def each_row(self):
        """Iterate rows"""
        for row in self.data:
            logger.debug(f"Row: {row[0]}")
            view_id = (row[0])
            self.data = fetch(
                    f"SELECT [SENSOR_ID],[NAME],[ACTIVE] FROM [QUICKVIEW_DB]."
                    f"[dbo].[VIEW_SENSORS] WHERE VIEW_ID = '{view_id}' and "
                    f"ACTIVE = 'TRUE'"
                    )
            self.each_sensor()

    def each_sensor(self):
        """Iterate through sensors"""
        for sensor in self.data:
            self.ID = (sensor[0])
            self.sensor_name = sensor[1]
            self.data = fetch(
                    f"SELECT [SENSOR_ID] FROM [QUICKVIEW_DB].[dbo]."
                    f"[SENSOR] WHERE ID = '{self.ID}'"
                    )
            self.each_data()

    def each_data(self):
        """

        :return:
        """
        if self.data:
            self.data = fetch(
                    f"SELECT TOP 1 [SENSOR_ID],[MEASURE_DATE],[VALUE],"
                    f"[VALUE_X],[VALUE_Y],[INSERTED_AT],[UPDATED_AT] FROM "
                    f"[QUICKVIEW_DB].[dbo].[MEASURE_VALUES] WHERE "
                    f"SENSOR_ID = "
                    f"'{self.data[0][0]}' ORDER BY MEASURE_DATE DESC"
                    )
            self.each_output()

    def each_output(self):
        """Output data"""
        if self.data:
            if WatchdogTime > self.data[0][1] > StaleTime:
                store(self)
                logger.info(
                        f"[{self.name},"
                        f"[{self.ID},"
                        f"{self.sensor_name},"
                        f"{self.data[0][1]},"
                        f"{self.data[0][2]},"
                        f"{self.data[0][3]},"
                        f"{self.data[0][4]}]"
                        )
            else:
                logger.debug(
                        f"Project: {self.name}; "
                        f"Sensor: {self.sensor_name}; "
                        f"Sensor ID: {self.data[0][0]}; "
                        f"Sensor timestmap: {self.data[0][1]}"
                        )


def main():
    """ Main """
    projects = fetch(
            f"SELECT [ID],[NAME],[ACTIVE] FROM "
            f"[QUICKVIEW_DB].[dbo].[PROJECTS] "
            f"WHERE ACTIVE = 'TRUE'")
    for each in projects:
        logger.debug(each[1])
        job = each_project(each)
        job.each_row()

    # Close out the json file once run is complete
    with open(store_path, 'a') as file:
        file.write(']')
        file.close()
    logger.info(f'Data dumped to {store_path}')


if __name__ == "__main__":
    """Prevents main from running unintentionally"""
    remove_file(store_path)
    logger = make_logger()
    logger.info(f'{filedate} ---- Log file for {__name__} - '
                f'logging level is {logger.getEffectiveLevel()}')
    logger.debug('Run start')
    main()
    post('log','QV List updated')
