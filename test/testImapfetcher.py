
import unittest

import mailindicator.imapfetcher


class TestImapfetcher(unittest.TestCase):

    def testConnection(self):
        HOST = 'localhost'
        USERNAME = 'username'
        PASSWORD = 'password'
        PORT = '1143'

        kwargs = {}
        kwargs['username'] = USERNAME
        kwargs['passwd'] = PASSWORD
        kwargs['host'] = HOST
        kwargs['port'] = PORT

        fetcher = mailindicator.imapfetcher.ImapFetcher('Test', **kwargs)

        # mails = fetcher.fetchmail()

        try:
            mails = fetcher.fetchmail()
        except Exception, e:
            print e

        for mail in mails:
            print mail


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
