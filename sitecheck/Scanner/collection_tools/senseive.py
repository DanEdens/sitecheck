"""
    Tools for interfacing with the AMTS1 server
"""

import datetime
import glob
import os
import sys

import utlis

today = datetime.datetime.utcnow()
filedate = today.strftime("%Y/%m")
root = r"\\172.16.16.10\collection_data\LOGGERNET1\Argus\senceive\ArchiveData"


def recent_data(_project='list', _pattern=filedate, _root=root):
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
        os.chdir(_project)
        list_of_files = glob.glob(
            '*.txt')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)

        with open(latest_file) as data:
            lines = data.readlines()
            for line in lines:
                # line_lengh = abs(8 - len(line))
                if str(_pattern) in line:
                    # date = line[82:98]
                    # sensor = line[2:-line_lengh]
                    # short_line = f'{sensor} | {date}'
                    contents.append(line)
                    print(line)
    return contents


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
