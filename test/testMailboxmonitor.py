from mailindicator.gmailfeedfetcher import GMailFeedFetcher
from mailindicator.mailboxmonitor import MailboxMonitor
from mailindicator.statusicon import StatusIcon
import os
import unittest


class TestMailboxmonitor(unittest.TestCase):


    def testStatusIconError(self):
        status_icon = StatusIcon()
        
        #os.environ['https_proxy'] = 'http://127.0.0.1:3030'
        fetcher = GMailFeedFetcher('alessio.piccoli', 'Echo09.box3')
        
        mb_monitor = MailboxMonitor(status_icon, 'TEST', 30, fetcher.fetchmail)
        mb_monitor.start()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()