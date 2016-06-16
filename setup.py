#!/usr/bin/python3
"""
  Author: Alessio Piccoli <alepic@geckoblu.net>

  This script needs python-distutils-extra, an extension to the standard
  distutils which provides i18n, icon support, etc.

  https://launchpad.net/python-distutils-extra
"""

from distutils.version import StrictVersion

try:
    import DistUtilsExtra.auto
except ImportError:
    import sys
    sys.stderr.write(
            'To build mailindicator you need https://launchpad.net/python-distutils-extra\n')
    sys.exit(1)

assert StrictVersion(DistUtilsExtra.auto.__version__) >= '2.4', 'needs DistUtilsExtra.auto >= 2.4'

DistUtilsExtra.auto.setup(
    name='mailindicator',
    version='0.1',
    description="Monitors mailboxes for new mail.",
    long_description="Monitors mailboxes for new mail.",
    url="http://www.geckoblu.net/html/mailindicator.html",
    license='GPL v3 or later',
    author="Alessio Piccoli",
    author_email="alepic@geckoblu.net",
    packages=['mailindicator']
)
