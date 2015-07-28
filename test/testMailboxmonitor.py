from mailindicator.gmailfeedfetcher import GMailFeedFetcher
from mailindicator.mailboxmonitor import MailboxMonitor
from mailindicator.statusicon import StatusIcon
import unittest


class TestMailboxmonitor(unittest.TestCase):

    def testStatusIconError(self):
        status_icon = StatusIcon()

        fetcher = GMailFeedFetcher('username', 'password')

        mb_monitor = MailboxMonitor(status_icon, 'TEST', 30, fetcher.fetchmail)
        mb_monitor.start()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
