:tocdepth: 2

==========================================================
Scripting with the Scanner module
==========================================================

Introduction
==========================================================

This project is devolped as 3 seperate modules and can be utlized indivually

Each package contains a __init__.py file, which acts as entry point and
information exchange to the component package.

Consists of one top-level package, sitecheck.
sitecheck is the scirpting that controls the gathering of data,

usually containing sub-packages. That top-level package usually
shares the name of your project, and exists as a directory in the
root of your project's repository.

BrowserContext
-----------------------------------

BrowserContext refers to the browser window itself.
This object has an unique ID when it is created that cannot currently be re-aquired once lost/destroyed.


Useful members
--------------


Useful functions
----------------

