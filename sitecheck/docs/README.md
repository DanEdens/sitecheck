
![](resources/logo-graphic.png)
# Sitecheck Scanner
#### Intended for Geo-Instruments Internal use

__author__ = Dan Edens
__version__ = 0.8.1.2

---
# Description
This tool provides convenient and interactive
troubleshooting tools for AMP and QV

It provides a Sensor status report in the form of an
[Adaptive Cards](https://docs.microsoft.com/en-us/power-automate/overview-adaptive-cards) to the user through Microsoft Teams.

![](resources/Cardexample.jpg)  
This is done by creating a Json file in the user's Keller - OneDrive.


The user can than prompt the Flowbot to ingest the data via the Team's chat, review it,  
and than pass it on to the Regional team.
```
run flow 1
```
![](resources/Run flow 1.jpg)

---

# INstallation

```
pip install sitecheck
```
Than use "run" followed by your options
```
run --verbose -p upsondrivevms
```

---
# Power Automate Import instructions

### Description

[Power Automate](https://docs.microsoft.com/en-us/power-automate/) is the platform that handles ingesting the cards from OneDrive and posting to chat.  
It is an included part of our Microsoft package, and functions within the group security policies.

# Install
## Flow script Import.

[Follow this link to import the included Package](Flow/ImportPackage.url)
---

![](resources/importpackage1.jpg)

Select [Scanner_flow.zip](Flow/Scannerflow.zip) file from your desktop
---

![](resources/importpackage2.jpg)


Select "create as new" and add your email to the connectors.
---
![](resources/importpackage3.jpg)

Follow the link in the success message.
```
  All package resouces were successfully imported.
The Flow has been created succesfully. Run the flow to make sure it's working. Open Flow
```

![](resources/importpackage4.jpg)

---

Change the value in "Intialize variable 2" to your Username.  
Can be tested by running the following in cmd
```
echo %USERPROFILE%
```

---
![](resources/importpackage5.jpg)

This needs to match to your Onedrive path.
```
C:\Users\%USERPROFILE%\OneDrive - Keller\scanner
C:\Users\Dan.Edens\OneDrive - Keller\scanner
```
---


Please report any bugs to Dan.Edens@geo-instruments.com


