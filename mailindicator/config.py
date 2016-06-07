"""-"""
import os
import xdg.BaseDirectory
import lxml.etree as etree

from mailindicator.mimailbox import Mailbox


XDG_RESOURCE = 'mailindicator'
XDG_CONFFILENAME = 'config.xml'

# Default configuration values ------------------------------------------------
mailboxes = []
use_proxy = False
http_proxy = ''
https_proxy = ''


def load(conffile=None):
    """Load configuration from file."""
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
    """Save configuration to file."""
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
    globalelement = root.find('global')
    if globalelement is not None:

        # Proxy -----------------------------------------------------------
        proxyelement = globalelement.find('proxy')
        if proxyelement is not None:
            use_proxy = proxyelement.get('use_proxy', False)
            http_proxyelement = proxyelement.find('http_proxy')
            if http_proxyelement is not None:
                http_proxy = http_proxyelement.text
            https_proxyelement = proxyelement.find('https_proxy')
            if https_proxyelement is not None:
                https_proxy = https_proxyelement.text
            _set_proxy_environment()

    # Mailboxes -----------------------------------------------------------
    mailboxes = []
    for mailboxelement in root.findall('mailboxes/mailbox'):
        mailboxes.append(Mailbox(**mailboxelement.attrib))


def _create_elementtree():
    root = etree.Element(XDG_RESOURCE)
    root.set('version', '1.0')
    root.append(etree.Comment('Configuration file for mailindicator'))

    # Global options ----------------------------------------------------------
    globalelement = etree.SubElement(root, 'global')

    # Proxy -------------------------------------------------------------------
    proxyelement = etree.SubElement(globalelement, 'proxy')
    proxyelement.set('use_proxy', str(use_proxy))
    http_proxyelement = etree.SubElement(proxyelement, 'http_proxy')
    http_proxyelement.text = http_proxy
    https_proxyelement = etree.SubElement(proxyelement, 'https_proxy')
    https_proxyelement.text = https_proxy

    # Mailboxes ---------------------------------------------------------------
    mbs = etree.SubElement(root, 'mailboxes')

    for mailbox in mailboxes:
        mbox = etree.SubElement(mbs, 'mailbox')
        mbox.set('typ', mailbox.type)
        mbox.set('label', mailbox.label)
        mbox.set('sleep_time', str(mailbox.sleep_time))
        for attribute_name, attribute_value in mailbox.get_attributes_to_store():
            mbox.set(attribute_name, str(attribute_value))

    # Create tree -------------------------------------------------------------
    tree = etree.ElementTree(root)
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
