|image1|

================================================================================
Sitecheck Scanner
================================================================================


* Intended for `Geo-Instruments <https://www.geo-instruments.com/>`__ Internal use


**Author** = Dan Edens

**Version** = 0.8.2


.. image:: https://img.shields.io/readthedocs/sitecheck?style=plastic   :alt: Read the Docs


.. image:: https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability
   :target: https://codeclimate.com/github/codeclimate/codeclimate/maintainability
   :alt: Maintainability

.. image:: https://img.shields.io/github/downloads/DanEdens/Sitecheck_Scrapper/total   :alt: GitHub All Releases



Description
----------------------------------------------------------------
This tool provides troubleshooting tools for AMP and QV

Setup to automatically scan a list of projects
and gather the most recent timestamp.

Sensor status reports in the form of an
`Adaptive Cards <https://docs.microsoft.com/en-us/power-automate/overview-adaptive-cards>`__
to each user through Teams.

To Stay informed in the field, and ease the process of requesting help


|cardexample|

These cards can be setup with options to get information to the right people,




Installation
----------------------------------------------------------------

::

    pip install sitecheck


If your python Bin is in your %PATH%, 'scanner' can now be called from anywhere. Read more about Argument options here

::

    scanner --debug --time 12 --project upsondrivevms

----------------------------------------------------------------


Power Automate Import instructions
==================================


    TODO: Section for copying from team_flow version

`Power Automate <https://docs.microsoft.com/en-us/power-automate/>`_ is the platform that handles ingesting the cards from OneDrive and posting to chat.
It is an included part of our Microsoft package, and functions within the group security policies.


`Follow this link to import the included Package <https://us.flow.microsoft.com/manage/environments/Default-b44eb401-1c30-454c-ae94-78de08e2320c/flows/import>`__


|image1|

Select the file - `Scannerflow.zip <Flow/Scannerflow.zip>`_

|image2|

Select "create as new" and add your email to the connectors.

|image3|

Follow the link in the success message.

::

    All package resouces were successfully imported.
    The Flow has been created succesfully. Run the flow to make sure its working. Open Flow

|image4|

----------------------------------------------------------------

Change the value in "Intialize variable 2" to your Username.
Can be checked by running the following in cmd

::

    echo %USERPROFILE%


|image5|

This needs to match to your Onedrive path, as in this example:

::

    C:\Users\%USERPROFILE%\OneDrive - Keller\scanner
    C:\Users\Dan.Edens\OneDrive - Keller\scanner


The user can now prompt the Flowbot to ingest the data via the Team's chat, review it,
and than pass it on to the Regional team.

::

    Run flow 1


|runflow1|


Please send your suggestions/questions to `Dan Edens@geo`_.

Bugs should be reported on the `Issues board <https://geodev.geo-instruments.com/DanEdens/Sitecheck\_Scanner/-/issues>`_
so they can be addressed by the team.



----------------------------------------------------------------

.. |image1| image:: _static/logo-graphic.png
    :width: 400

.. |image2| image:: _static/Importpackage1.jpg

.. |image3| image:: _static/Importpackage2.jpg

.. |image4| image:: _static/Importpackage3.jpg

.. |image5| image:: _static/Importpackage4.jpg

.. |runflow1| image:: _static/Runflow1.jpg

.. |cardexample| image:: _static/Cardexample.jpg

.. _Dan Edens@geo: Dan.edens@geo-instruments.com
