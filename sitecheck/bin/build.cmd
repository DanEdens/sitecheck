@echo off
CHOICE /C:01 /m "Run Build? [1]yes or [0]No"
    goto sub_%ERRORLEVEL%

:sub_0
    python setup.py
    GOTO:eof
:sub_1
    echo okay
    GOTO:eof
