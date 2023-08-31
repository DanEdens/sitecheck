"""
    utliies used by the AMTS1 server tools
"""
import os


def list_directories(path='.'):
    """ A function that lists the directories """
    dir_list = next(os.walk(path))[1]
    for index, dirs in enumerate(dir_list):
        print(index + 1) + ") ", dirs
    return dir_list


def file_read_from_tail(fname, lines=-1):
    """ read last n lines of a file. """
    bufsize = 8192
    fsize = os.stat(fname).st_size
    _iter = 0
    with open(fname) as f:
        if bufsize > fsize:
            bufsize = fsize - 1
            data = []
            while True:
                _iter += 1
                f.seek(fsize - bufsize * _iter)
                data.extend(f.readlines())
                if len(data) >= lines or f.tell() == 0:
                    print(''.join(data[-lines:]))
                    break
