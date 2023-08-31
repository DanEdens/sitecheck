@echo OFF

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "date=%YYYY%-%MM%-%DD%"

if '%~1'=='' (
    SET /P project=Enter project name:
) ELSE (
    SET project=%1
)

if project=='list' (
    echo No Project. Listing..
    pushd \\172.16.16.10\collection_data\\AMTS1\\monstar2\\
    dir /B
    cmd
    exit
    )

if '%~2'=='' (
    SET /P prism=Enter filter:
) ELSE (
    SET prism=%2
)

if %prism%==' '( set prism='2020')

pushd \\172.16.16.10\collection_data\\AMTS1\\monstar2\\%project%\\CurrentAdj

type *.dat |findstr /r %date% |findstr /r %prism%*

popd

