from lxml.etree import ElementTree, Element, Comment
from mailindicator.mimailbox import Mailbox
import os
import xdg.BaseDirectory

import lxml.etree as etree


XDG_RESOURCE = 'mailindicator'
XDG_CONFFILENAME = 'config.xml'

# Default configuration values ------------------------------------------------
mailboxes = []
use_proxy = False
http_proxy = ''
https_proxy = ''


def load(conffile=None):
    if not conffile:
        conffile = _get_confifle_name()

    if conffile:
        tree = etree.parse(conffile)
        _parse_elementtree(tree)
    else:
        # Use default values
        # TODO First time show config dialog
        pass


def save(conffile=None):
    if not conffile:
        confpath = xdg.BaseDirectory.save_config_path(XDG_RESOURCE)
        conffile = os.path.join(confpath, XDG_CONFFILENAME)

    if conffile:
        tree = _create_elementtree()
        tree.write(conffile, xml_declaration=True, pretty_print=True)
    else:
        raise Exception('No conffile found.')


def _parse_elementtree(tree):
    global mailboxes, use_proxy, http_proxy, https_proxy
    root = tree.getroot()

    # Global options ------------------------------------------------------
    globalElement = root.find('global')
    if globalElement is not None:

        # Proxy -----------------------------------------------------------
        proxyElement = globalElement.find('proxy')
        if proxyElement is not None:
            use_proxy = proxyElement.get('use_proxy', False)
            httpproxyElement = proxyElement.find('http_proxy')
            if httpproxyElement is not None:
                http_proxy = httpproxyElement.text
            httpsproxyElement = proxyElement.find('https_proxy')
            if httpsproxyElement is not None:
                https_proxy = httpsproxyElement.text
            _set_proxy_environment()

    # Mailboxes -----------------------------------------------------------
    mailboxes = []
    for mailboxElement in root.findall('mailboxes/mailbox'):
        mailboxes.append(Mailbox(**mailboxElement.attrib))


def _create_elementtree():
    root = Element(XDG_RESOURCE)
    root.set('version', '1.0')
    root.append(Comment('Configuration file for mailindicator'))

    # Global options ----------------------------------------------------------
    globalElement = etree.SubElement(root, 'global')

    # Proxy -------------------------------------------------------------------
    proxyElement = etree.SubElement(globalElement, 'proxy')
    proxyElement.set('use_proxy', str(use_proxy))
    httpproxyElement = etree.SubElement(proxyElement, 'http_proxy')
    httpproxyElement.text = http_proxy
    httpsproxyElement = etree.SubElement(proxyElement, 'https_proxy')
    httpsproxyElement.text = https_proxy

    # Mailboxes ---------------------------------------------------------------
    mbs = etree.SubElement(root, 'mailboxes')

    for mailbox in mailboxes:
        mb = etree.SubElement(mbs, 'mailbox')
        mb.set('typ', mailbox.type)
        mb.set('label', mailbox.label)
        mb.set('sleep_time', str(mailbox.sleep_time))
        for attribute_name, attribute_value in mailbox.get_attributes_to_store():
            mb.set(attribute_name, str(attribute_value))

    # Create tree -------------------------------------------------------------
    tree = ElementTree(root)
    # etree.dump(root)
    return tree


def _get_confifle_name():
    conffile = None
    confpath = xdg.BaseDirectory.load_first_config(XDG_RESOURCE)
    if confpath:
        conffile = os.path.join(confpath, XDG_CONFFILENAME)
        if not os.path.isfile(conffile):
            conffile = None
    return conffile


def _set_proxy_environment():
    if use_proxy:
        if http_proxy and http_proxy.strip() != '':
            os.environ['http_proxy'] = http_proxy
        if https_proxy and https_proxy.strip() != '':
            os.environ['https_proxy'] = https_proxy
