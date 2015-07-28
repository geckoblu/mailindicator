import mailindicator.imapstarttlsfetcher
import unittest


class TestImapstarttlsfetcher(unittest.TestCase):

    def testConnection(self):
        HOST = 'hostname'
        USERNAME = 'username'
        PASSWORD = 'password'

        fetcher = mailindicator.imapstarttlsfetcher.ImapStartTlsFetcher(USERNAME, PASSWORD, HOST)

        try:
            mails = fetcher.fetchmail()
        except Exception, e:
            print e

        for mail in mails:
            print mail


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
