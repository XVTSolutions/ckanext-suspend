ckanext-suspend
===============
Allows datasets to be suspended
+ adds Suspend button to dataset edit page
+ only users with permission to edit datasets can suspend one
+ adds a package_suspend table to db. This is used to store the reason for the suspension.

Installation
-------------
1. clone this repository
2. install: `python ckanext-suspend/setup.py develop`
3. add `suspend` to the list of plugins in .ini file

