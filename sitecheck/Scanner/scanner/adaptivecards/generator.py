"""
This module is apart of the Sitecheck Scanner project

:author:  Dan Edens @DanEdens <Dan.Edens@geo-instruments.com>
:synopsis: generator.py: Library for generating JSON cards from a template.
Guide on Message Cards: https://docs.microsoft.com/en-us/adaptive-cards/

This module stores sensor data in temp during run,
and than generates a Team's Adaptive Card.
The card is ingested into Team's via Flowbot through OneDrive
and sent to the user's private channel.
"""
import json
import logging
import os
from json import JSONDecodeError
from pathlib import Path

from dateutil.parser import parse

logger = logging.getLogger('generator')
from sitecheck.Scanner.scanner import utlis
from . import template


class SensorDataFormatter:
    """
    Converts args into tuple before applying the template and returning
    as Adaptive Card Json table

    :param name: Sensor ID
    :type name: str

    :param color: Examples:'good','attention','warning'
    :type color: str

    :param status: Examples:'Up-to-date', 'Behind', 'Older than a week'
    :type status: str

    :param time: str(parse(text.nowdate)) Examples: '2020-01-14 08:00:00'
    :type time: str


    :returns:(sudo json)
            Sensor data in Card format block
    :rtype: str
    """

    def __init__(self, name, color, status, time):
        self.name = name
        self.color = color
        self.status = status
        self.time = time

    def __str__(self):
        data_line: str = template.st1 + \
                         self.name + \
                         template.st2 + \
                         self.status + \
                         template.st3 + \
                         self.color + \
                         template.st4 + \
                         self.time + \
                         template.st5
        return str(data_line)


class Generator:
    """
        Builds the Adaptive card
    """

    def __init__(self, current_project):
        """
        :param current_project: Tuple comtaining projcet infomation
        :type current_project: Tuple

                project (str): Name to display at top of card
                store_path (str): Location of staged output. It will than be picked up by the Teams_hook.py
                generator_output (str): File path of output file
                url (str): Card button 'Project Website" target
        """
        self.project = current_project.name
        self.store_path = Path(f"{os.environ['Output']}//data"
                               f"//{os.environ['filedate']}"
                               f"//{self.project}.txt")
        utlis.ensure_exists(self.store_path)
        self.output_path = Path(f"{os.environ['Output']}//{self.project}.json")
        self.url = f'https://{self.project}.geo-instruments.com/index.php'

    def compile_data(self):
        """
            Adds the end bracket to finish list of lists
            Reads the finished product as string
            Converts String to List
            Returns call to generate the appropraite template

        :returns: generate_template with Json loaded from data storage
        :rtype: object
        """
        # Closes out the looping sensor data
        with open(self.store_path, 'a') as file:
            file.write(']')

        # Add the Card's tail.
        with open(self.store_path) as file:
            try:
                list_of_lists = file.read()
                card_list = json.loads(list_of_lists)
                return True
            except JSONDecodeError as e:
                # If no missing data, the json.load fails and
                # generate_empty_template is called.
                logger.debug(e)
                return False

    def generate_template(self, card_list):
        """
            Builds the Adaptive Teams Card
            Traditional tools for Json formatting do not preserve the template's syntax,
            So we are currently building manually
            For card_list, the sensor data is looped to create a table.
            This adds each sensor to the card and add a comma between them.
            Once the last run, the comma is skipped and the bracket is closed

            Needs Improvement:
                Using print to write is convenient insurance against missing
                line breaks when manually building json schematics

        :param card_list: List of sensor data in card template format [[name, color, status, time]]
        :type card_list: 2 dimensional list [[str, str, str, str]]

        :returns: path and filename of generated json file
        :rtype: str
        """
        with open(self.output_path, 'w') as gen_file:
            print(template.Top_prefix1 % self.project, file=gen_file)
            print(template.sensor_prefix, file=gen_file)
            _run = len(card_list)

            _loop = 0
            for e in card_list:
                data_info = SensorDataFormatter(e[0], e[1], e[2], e[3])
                _loop += 1
                if _loop != _run:
                    print(str(data_info) + ',', file=gen_file)
                else:
                    print(data_info, file=gen_file)
            print(template.sensor_suffix, file=gen_file)
            print(
                template.Link_row_template1 +
                self.project +
                template.Link_row_template2,
                file=gen_file
                )
            print(
                template.button_row_template1 +
                self.url +
                template.button_row_template2,
                file=gen_file
                )
            print(template.Bot_suffix, file=gen_file)
        return gen_file.name

    def generate_empty_template(self):
        """
        Generates a blank card if no missing Sensor data was stored.

        :returns: path of generated json file
        :rtype: str

        """
        with open(self.output_path, 'w') as gen_file:
            print(template.Top_prefix1 % self.project, file=gen_file)
            print(template.sensor_prefix, file=gen_file)
            nowdate = os.environ['Nowdate']
            data_info = SensorDataFormatter(
                'No Issues', 'good', 'Up-to-date', str(parse(nowdate))
                )
            print(data_info, file=gen_file)
            print(template.sensor_suffix, file=gen_file)
            print(
                template.Link_row_template1 +
                self.project +
                template.Link_row_template2,
                file=gen_file
                )
            print(
                template.button_row_template1 +
                self.url +
                template.button_row_template2,
                file=gen_file
                )
            print(template.Bot_suffix, file=gen_file)
        return gen_file.name
