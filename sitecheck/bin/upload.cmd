@echo off
CHOICE /C:01 /m "Which Repo? [1]testpypi or [0]pypi"
    goto sub_%ERRORLEVEL%

:sub_1
    echo Uploading to pypi
    twine upload --verbose dist/*.whl
    GOTO:eof
:sub_2
    echo Uploading to testpypi
    twine upload --verbose --repository testpypi dist/*.whl
    GOTO:eof

