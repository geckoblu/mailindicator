# Mailindicator

Monitors mailboxes for new mail.

http://www.geckoblu.net/html/mailindicator.html



## Installation

sudo aptitude install python3-lxml python3-xdg python3-feedparser libnotify4

mkdir -p ~/.config/mailindicator
cp ~/soft/ubuntu-install/installation-22.04/data/configuration_backup/user/mailindicator/config.xml ~/.config/mailindicator/



## Build debian package

Reference: [Use stdeb to make Debian packages for a Python package](https://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html)

sudo aptitude install python3-stdeb fakeroot dh-python build-essential

python3 setup.py --command-packages=stdeb.command bdist_deb


## References
[Use stdeb to make Debian packages for a Python package](https://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html)
[Packaging Python programs - DEB (and RPM) packages ](https://www.dlab.ninja/2015/11/packaging-python-programs-debian-and.html)
