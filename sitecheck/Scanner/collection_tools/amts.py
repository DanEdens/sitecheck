"""
    Tools for interfacing with the AMTS1 server
"""

import datetime
import os
import sys

from . import utlis

today = datetime.datetime.utcnow()
filedate = today.strftime("%Y-%m")
root = r"\\172.16.16.10\collection_data\AMTS1\monstar2"


def recent_data(_project='list', _pattern='MD', _root=root):
    """
    grep {filter} .dat in monstar2\\prjcet\\current_env
    equivelent in cmd 

    ''
        type *.dat |findstr /r %date% |findstr /r %prism%*

    :param: project: Project folder 
    :param: filter: Sensor to filter
    :returns: List of lines matching filter and filedate
    """

    contents = []
    os.chdir(_root)

    if _project == 'list':
        contents = utlis.list_directories()
    else:
        os.chdir(f"{_project}\\CurrentAdj")
        with open(f'{_project}.dat') as data:
            lines = data.readlines()
            for line in lines:
                line_lengh = abs(8 - len(line))
                if str(_pattern) and str(filedate) in line:
                    date = line[82:98]
                    sensor = line[2:-line_lengh]
                    short_line = f'{sensor} | {date}'
                    contents.append(short_line)
                    print(short_line)
    return contents


def recent_monstar(_project, lines=-30):
    """
    Get log output from most recent Monstar activity

    :param _project: Project name
    """
    os.chdir(f"{root}")
    os.chdir(f"{_project}")
    # x='tail - n 30 MonStarLE.log'
    with open('MonStarLE.log', 'r') as file:
        utlis.file_read_from_tail(file, lines)
        


if __name__ == "__main__":
    try:
        project = sys.argv[1]
    except IndexError:
        project = input("Project: ") or 'list'

    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = input("Pattern: ") or 'MD'

    recent_data(project, pattern)
