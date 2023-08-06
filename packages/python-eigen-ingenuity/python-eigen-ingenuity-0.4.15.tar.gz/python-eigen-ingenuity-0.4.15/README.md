python-eigen-ingenuity is a python library used to query data from the Eigen ingenuity system

REQUIREMENTS
============

python-eigen-ingenuity requires Python 2.X/3.X and nine

INSTALL
=======

The recommended method of installation on production systems is to use the generated .deb and RPM packages
since these contain all the correct dependency information, and are the easiest to integrate into ansible
and/or install onto existing systems.

LOCAL INSTALL
=============

Install python 2.X or 3.X  (in windows suggest you select the option to Add python.exe to path and reboot after python install.)
unzip the install to a folder then run pip (for python3 run pip3)
e.g. in windows

```
pip install C:\path\to\python-eigen-ingenuity -r requirements.txt
```

Third party libraries should be automatically installed through requirements.txt.

DEPENDENCIES
============

Unfortunately the pip requirements.txt doesn't appear to easily integrate with .deb and RPM packaging
systems and so currently dependencies need to be tracked in 3 places:

- requirements.txt
- debian/control
- setup.cfg.jenkins

Any suggestions as to how to improve this situation would be gratefully received.

EXAMPLE
-------

Go to the examples folder and copy example-python-to-eigen-ingenuity.py modify the eigen-ingenuity server and tags then run
python example-python-to-eigen-ingenuity.py

license
(c)2016-2018 Eigen Ltd. No redistribution without permission
