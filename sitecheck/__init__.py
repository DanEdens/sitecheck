"""
    init file for Join-CLi
"""
# __name__ = 'join'

import os
import sys
import datetime

# Set the current working directory as the ROOT_DIR environment variable
os.environ['ROOT_DIR'] = os.getcwd()

# Set the filedate and Nowdate environment variables using the current date and time
filedate = datetime.datetime.utcnow().strftime("%Y-%m-%d")
os.environ['filedate'] = filedate
nowdate = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
os.environ['Nowdate'] = nowdate

# Add the current working directory to the list of directories to search for modules
sys.path.insert(0, os.environ['ROOT_DIR'])
