"""
    Geo-Instruments
    Sitecheck Scanner

Loads program configuration as a project.tuple object

Config file looks for file in the following hierarchy:
1. Argument
2. Default
3. File_dialog
4. Generate_default

http://docs.python.org/library/configparser.html

"""
import configparser
import os.path
import subprocess
import sys
import logging

import paho.mqtt.client as mqtt

from . import projectstore

hostname = os.environ.get('awsip')
port = int(os.environ.get('awsport', '-1'))
client = mqtt.Client("qv", clean_session=True)
client.connect(hostname, port)

logger = logging.getLogger('config')


def edit_project():
    """
    Subprocess edit Project configuration file in notepad.

    ::returns:: Edit subprocess returncode
    """
    logger.info("Project config file opened. Please close to continue..")
    if os.path.exists(projectstore):
        if os.supports_bytes_environ:
            subprocess.Popen(["mousepad", projectstore]).wait()
        else:
            return subprocess.run(f'notepad.exe {projectstore}').returncode


# def generate_default():
#     """
#     Generates a default ini config file as a fallback to the included copy being removed.
#     User is presented chance to edit the new file in notepad before continuing
# 
#     ::returns:: Edit subprocess returncode
#     """
#     config = configparser.ConfigParser()
#     config['DEFAULT'] = {}
#     config['DEFAULT']['name'] = 'Test'
#     config['DEFAULT']['planarray'] = '0'
#     config['DEFAULT']['site'] = 'qv'
#     config['DEFAULT']['skip'] = 'false'
#     with open('projects.ini', 'w') as configfile:
#         config.write(configfile)
#     return edit_project()


def edit_config_option(project, option, value):
    """
    Change an option in the projects.ini file
    :param project: Project who's config to edit
    :param option: Option to edit
    :param value: New value of the option
    Example - edit_config_option(
    """
    config = configparser.ConfigParser()
    config.read(projectstore)
    config[project][option] = value
    try:
        with open(projectstore, 'w') as configfile:
            config.write(configfile)
            logger.debug(f'Editted config file: {project}, {option}, {value}')
    except configparser.Error as err:
        return err


def file_dialog():
    """
        Check and use Tkinter for file dialog, or call generate_default.

        ::returns:: filename
    """
    try:
        import tkinter
        from tkinter import filedialog

        options = {}
        options['defaultextension'] = '.ini'
        options['filetypes'] = [('ini config files', '.ini')]
        options['initialdir'] = os.environ['ROOT_DIR']
        options['initialfile'] = 'projects.ini'
        options['title'] = 'Select Project Configuration File'
        root = tkinter.Tk()
        filename = filedialog.askopenfilename(**options)
        root.destroy()
        return filename
    except ImportError:
        pass


def read_config_file():
    """
    Prompts user to select projects.ini configuration and returns contents as list
    Default projects.ini is ROOT_DIR+"\\project.ini"

    :rtype: list
    """
    if os.path.isfile(projectstore):
        config_file = projectstore
    else:
        config_file = file_dialog()

    if config_file == '':
        sys.exit("No Config selected. Exiting..")
    elif not os.path.isfile(config_file):
        logger.warning("file (%s) not found. " % config_file)
        sys.exit("Exiting..")

    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except configparser.DuplicateSectionError as e:
        logger.warn('Duplicate Section Error found in config, '
                    'Please locate the error in notepad \n' + str(e))
        edit_project()
        logger.warn("Rerunning config check..")
        read_config_file()
    except configparser.DuplicateOptionError as e:
        logger.warn('Duplicate Setup found in config, '
                    'Please locate the error in notepad \n' + str(e))
        edit_project()
        logger.warn("Rerunning config check..")
        read_config_file()

    return config


# def check_credentials():
#     """
#     Prompt for User and password if not preset as environmental variables.
# 
#     :return: err code
#     :rtype: Int
#     """
#     if not os.environ['SCANNER_AMPUSER']:
#         os.environ['SCANNER_AMPUSER'] = input("Amp Username:")
#     if not os.environ['SCANNER_AMPPASS']:
#         os.environ['SCANNER_AMPPASS'] = input("Amp Password:")
#     if not os.environ['SCANNER_QVUSER']:
#         os.environ['SCANNER_QVUSER'] = 'admin'
#         print('Qv user set \'admin\'')
#     if not os.environ['SCANNER_QVPASS']:
#         os.environ['SCANNER_QVPASS'] = input("QV Password:")
#         save = input("Save for future runs? (y/n)")
#     if save == 'y':
#         return save_credentials()
#     else:
#         return 0


# def save_credentials():
#     """
#     Attempts to create a batch file to setx values to system.
#     :return: err code
#     :rtype: Int
#     """
#     with open('env.cmd', 'a') as file:
#         file.write('setx ' + os.environ['SCANNER_AMPUSER'])
#         file.write('setx ' + os.environ['SCANNER_AMPPASS'])
#         file.write('setx ' + os.environ['SCANNER_QVUSER'])
#         file.write('setx ' + os.environ['SCANNER_QVPASS'])
#         file.write('del %0')
#         file.close()
#     set_env = subprocess.run('env.cmd', check=True).returncode
#     if set_env != 0:
#         logger.error("Creds autosave has failed. "
#                      "\nPlease manually set using setx \n"
#                      "\nsetx SCANNER_AMPUSER \"Jane Doe\""
#                      "\nsetx SCANNER_AMPUSER ThisPassword"
#                      "\nsetx SCANNER_QVUSER admin"
#                      "\nsetx SCANNER_QVUSER AnotherPassword"
#                      "\n You will need to restart cmd after doing so")
#     return set_env


class tuple_from_section_config:
    """
    Create's tuple object from given section "project"
    ::return:: self
    """

    def __init__(self, project):
        if os.environ['SCANNER_CONFIG'] == 'mqtt':
            self.name = client.subscribe(
                f'Scanner/config/{project}/name')
            self.planarray = client.subscribe(
                f'Scanner/config/{project}/planarray')
            self.site = client.subscribe(
                f'Scanner/config/{project}/site')
            self.skip = client.subscribe(
                f'Scanner/config/{project}/skip')
        else:
            config = configparser.ConfigParser()
            config.read(projectstore)
            self.name = config[project]['name']
            self.planarray = config[project]['planarray']
            self.site = config[project]['site']
            self.skip = config[project]['skip']
        # elif os.environ['SCANNER_CONFIG'] == 'mqtt':
