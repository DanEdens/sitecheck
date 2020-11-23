"""
    Geo-Instruments
    Sitecheck Scanner
    Command Line argument Parser for Scanner
    Provides handling of arguments passed from command line
    These can be made permenant by adding them to your shortcut path

"""
import argparse
import logging
import platform
import os
from pathlib import Path

from . import config
from . import utlis

logger = logging.getLogger('config')
projects = config.read_config_file()
system = platform.system()

if system == "Linux":
    ROOT_card: str = utlis.ensure_exists(str(Path("~//Scanner//")))
elif system == "Windows":
    ROOT_card: str = utlis.ensure_exists(str(
            Path(os.environ['OneDriveCommercial'] + "//Scanner//")
            ))

data_choice = [
    'mqtt', 'print',
    'file', 
    # 'card',
    # 'list'
    ]


chrome_args = ['--window-size=1980,944']  # '--kiosk''


class Formatter(argparse.RawDescriptionHelpFormatter):
    """argparse.RawDescriptionHelpFormatter
        Provides formatting settings for argument "Help" messages.
        Can add argparse.ArgumentDefaultsHelpFormatter for defaults.
    """
    pass


class EnvDefault(argparse.Action):
    """ Allows arguments to be set by env variable """

    def __init__(self, envvar, required=False, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class arg_text:
    """ Text for --help """
    output: str = 'Set output directory, Defaults to onedrive//scanner'
    reset: str = 'Re-enable all projects'
    main: str = """
    Automated Sitecheck Toolkit for Geo-Instruments Field Technicians
    \nSensors are sorted into three categories:
    \nUp-to-date:    Most recent data is within 24 hours
    \nOverdue:       Instrument is behind
    \nOld:           Reading has been missing for over a week
    \nAn Adaptive card containing missing sensor information is sent the user via Microsfot Team's Flowbot
    \nUser can push Cards into their Regional Sitecheck channel of choice.
    """
    info: str = 'Set logging level to Info'
    debug: str = 'Set logging level to Debug'
    log: str = f'Saves stout to log file located at \"{ROOT_card}' \
               '/data/filedata/run_report.log\"'
    edit: str = 'Opens projects file in editor'
    project_builtins: str = 'force, qv, amp'
    project: str = f'Define a single project to run. Availble Options include {project_builtins} ' \
                   f'Options: {str(projects.sections())}. '
    time: str = 'Set number of hours to mark as \'Up-to-date\' \n ' \
                '\'Old\' is a 7 times multiple of this value. ' \
                'Example: --time 24'
    data: str = 'Selects Output format --data=\'mqtt\''
    test: str = 'Run program up until time of browser creation ' \
                'for testing purposes.'
    repl: str = 'read–eval–print loop (REPL) Interactive command mode'
    old: str = 'Include in report sensors missing for Longer than a week. ' \
               'This is off by default, Assumes sensors missing for 7 days ' \
               'are discussed.'
    new: str = 'Include in report sensors that pass checks. This is off by ' \
               'default to prevent unnecessary spam'
    headless: str = 'Enables Pyppeteer\'s Headless mode. The browser ' \
                    'will run invisibly, Known Issues with Qv navigation ' \
                    'are being addressed'
    putput: str = 'Set card output directory'
    value: str = 'Include current Sensor data in output'
    weather: str = 'Include local weather data in status report'
    sensor: str = 'Stop run when this Sensor name is found'
    screenshot: str = 'Save a screenshot when a sensor is missing'


parser = argparse.ArgumentParser(
    description=arg_text.main,
    prog='Sitecheck Scanner',
    formatter_class=Formatter
    )

parser.add_argument('-r', '--repl', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_text.repl)

parser.add_argument('-H', '--headless', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_text.hadless)

parser.add_argument('-i', '--info', action='store_true', default=True,
                    help=arg_text.info)

parser.add_argument('-d', '--debug', action='store_true', default=False,
                    help=arg_text.debug)

parser.add_argument('-l', '--log', action='store_true', default=False,
                    help=arg_text.log)

parser.add_argument('-e', '--edit', action='store_true', default=False,
                    help=arg_text.edit)

parser.add_argument('-p', '--project', default='All',
                    choices=projects.sections(), metavar='',
                    help=arg_text.project)

parser.add_argument('--detach', default='',
                    type=str,
                    metavar='',
                    help=arg_text.sensor)

parser.add_argument('-t', '--time', default='24', metavar='', type=int,
                    help=arg_text.time)

parser.add_argument('--test', action='store_true', default=False,
                    help=arg_text.test)

parser.add_argument('--reset', action='store_true', default=False,
                    help=arg_text.reset)

parser.add_argument('-O', '--old', action='store_true', default=False,
                    help=arg_text.old)

parser.add_argument('-N', '--new', action='store_true', default=False,
                    help=arg_text.new)

parser.add_argument('-o', '--output', action='store', type=str, metavar='',
                    default=ROOT_card,
                    help=arg_text.output)

parser.add_argument('--data', default='mqtt',
                    choices=data_choice, metavar='',
                    help=arg_text.data)

parser.add_argument('-v', '--value', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_test.value)

parser.add_argument('-s', '--screenshot', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_test.screenshot)

parser.add_argument('--pipeline', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_test.pipeline)

args = parser.parse_args()

os.environ['imagelist'] = 'fakesensor1,fakesensor2'
os.environ['SCANNER_OUTPUT_TYPE'] = str(args.data)
os.environ['Pipeline']: str = str(args.pipeline)
os.environ['Repl']: str = str(args.repl)
os.environ['Edit']: str = str(args.edit)
os.environ['Reset']: str = str(args.reset)
os.environ['Output']: str = args.output
os.environ['DETACH']: str = args.detach
os.environ['Headless']: str = str(args.headless)
Project: str = args.project
Info: bool = args.info
Debug: bool = args.debug
Log: bool = args.log
Test: bool = args.test
PrintOld: bool = args.old
PrintNew: bool = args.new
Getvalue: bool = args.value
Screenshot: bool = args.screenshot

Watchdog: int = int(args.time * 3600)
Oldperiod: int = 604800
