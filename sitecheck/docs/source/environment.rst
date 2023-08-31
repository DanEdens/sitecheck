Environment Documentation
============================

Sitecheck looks for certain environment variables to aid its operations.

To set creds:

type the following commands into your command line, or run in a batch file.
SETX SCANNER_AMPUSER <your user>
SETX SCANNER_AMPPASS <your pass>
SETX SCANNER_QVPASS <your user>
SETX SCANNER_QVPASS <your pass>

If these variables are not set, scanner will query and attempt to save
them by generating a temporary batch file.
This will request a UAC dialog, which may interupt the process.

Setting them yourself before hand is perfered method

