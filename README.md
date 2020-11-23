
![](sitecheck/docs/resources/logo-graphic.png?raw=true "Logo")

# Sitecheck Scanner
#### Intended for Geo-Instruments Internal use

[__Website__](https://github.com/DanEdens/Sitecheck_Scrapper)

__author__ = Dan Edens
__version__ = 0.8.2

[![Documentation Status](https://readthedocs.org/projects/sitecheck/badge/?version=latest)](https://sitecheck.readthedocs.io/en/latest/?badge=latest)


[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)


---
# Description
This tool provides troubleshooting tools for AMP and QV

Sensor status report in the form of an
[Adaptive Cards](https://docs.microsoft.com/en-us/power-automate/overview-adaptive-cards) to the user through Teams.

![](sitecheck/docs/resources/Cardexample.jpg)

These Sensor status reports currently come in the form of an
[Adaptive Cards](https://docs.microsoft.com/en-us/power-automate/overview-adaptive-cards)
pushed to each user through Teams.

This aims to enable us to stay informed in the field, and ease the process of
requesting help when accessiblity is limited.
![](sitecheck/docs/source/_static/Cardexample.jpg)

These cards can be setup with options for pipelining infomation to the right people,
keeping the team updated on site conditions.


# Installation

```
pip install sitecheck
```
'scanner' can now be called from anywhere. Read more about Argument options here
```
scanner --info -p upsondrivevms
```

---
# Power Automate Import instructions

## Flow script Import.

[Power Automate](https://docs.microsoft.com/en-us/power-automate/) is the platform that handles ingesting the cards from OneDrive and posting to chat.
It is an included part of our Microsoft package, and functions within the group security policies.


[Follow this link to import the included Package](https://us.flow.microsoft.com/manage/environments/Default-b44eb401-1c30-454c-ae94-78de08e2320c/flows/import)
---

![](sitecheck/docs/resources/importpackage1.jpg?raw=true "importpackage1")

Select [Scanner_flow.zip](Flow/Scanner_flow.zip) file from your desktop
---

![](sitecheck/docs/resources/importpackage2.jpg?raw=true "importpackage2")


Select "create as new" and add your email to the connectors.
---
![](sitecheck/docs/resources/importpackage3.jpg?raw=true "importpackage3")

Follow the link in the success message.
```
  All package resouces were successfully imported.
The Flow has been created succesfully. Run the flow to make sure it's working. Open Flow
```

![](sitecheck/docs/resources/importpackage4.jpg?raw=true "importpackage4")

---

Change the value in "Intialize variable 2" to your Username.
Can be tested by running the following in cmd
```
echo %USERPROFILE%
```

---
![](sitecheck/docs/resources/importpackage5.jpg?raw=true "importpackage5")

This needs to match to your Onedrive path.
```
C:\Users\%USERPROFILE%\OneDrive - Keller\scanner
C:\Users\Dan.Edens\OneDrive - Keller\scanner
```
---

The user can than prompt the Flowbot to ingest the data via the Team's chat, review it,
and than pass it on to the Regional team.
```
run flow 1
```
![](sitecheck/docs/source/_static/Runflow1.jpg)

---

Bugs should be reported on the [Issues board](https://geodev.geo-instruments.com/DanEdens/Sitecheck\_Scanner/-/issues)
so they can be addressed by the team.


