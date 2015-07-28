from mailindicator.mimailbox import Mailbox
import os
import tempfile
import unittest

import lxml.etree as etree
import mailindicator.config as config
from test.testconstants import TESTCONFIG


class TestConfig(unittest.TestCase):

    def test_get_confifle_name(self):
        conffile = config._get_confifle_name()
        assert conffile.endswith('config.xml')

    def test_set_proxy_environment(self):
        del os.environ['http_proxy']
        del os.environ['https_proxy']

        config.use_proxy = True
        config.http_proxy = 'http_proxy'
        config.https_proxy = 'https_proxy'

        config._set_proxy_environment()

        assert os.environ['http_proxy'] == 'http_proxy'
        assert os.environ['https_proxy'] == 'https_proxy'

    def test_parse_elementtree(self):
        tfile = tempfile.TemporaryFile()
        tfile.write(TESTCONFIG)
        tfile.seek(0)
        # print tfile.read()
        tree = etree.parse(tfile)
        tfile.close()
        config._parse_elementtree(tree)
        assert config.use_proxy
        assert config.http_proxy == 'http://127.0.0.1:3128'
        assert config.https_proxy == 'https://127.0.0.1:3128'
        assert len(config.mailboxes) == 3
        gmailfind = localmbox = imapstarttls = False
        for mb in config.mailboxes:
            if mb.type == Mailbox.GMAILFEED:
                gmailfind = True
                assert mb.label == 'GMAIL'
                assert mb.sleep_time == 300
                assert mb.enabled == True
                assert mb.username == 'testusername'
                assert mb.userpassword == 'testusserpassword'
            elif mb.type == Mailbox.LOCALMBOX:
                localmbox = True
                assert mb.label == 'System'
                assert mb.sleep_time == 60
                assert mb.enabled == False
                assert mb.mboxpath == '/var/spool/mail/testuser'
            elif mb.type == Mailbox.IMAPSTARTTLS:
                imapstarttls = True
                assert mb.label == 'Work'
                assert mb.sleep_time == 65
                assert mb.enabled == True
                assert mb.username == 'testusername'
                assert mb.userpassword == 'testuserpassword'
                assert mb.host == 'testhost.org'
        assert gmailfind
        assert localmbox
        assert imapstarttls


if __name__ == '__main__':
    unittest.main()
