
import unittest

import mailindicator.imapfetcher


class TestImapfetcher(unittest.TestCase):

    def testConnection(self):
        HOST = 'localhost'
        USERNAME = 'b02183'
        PASSWORD = 'Leonida123'
        PORT = '1143'

        kwargs = {}
        kwargs['username'] = USERNAME
        kwargs['userpassword'] = PASSWORD
        kwargs['host'] = HOST
        kwargs['port'] = PORT

        fetcher = mailindicator.imapfetcher.ImapFetcher('Test', **kwargs)

        # mails = fetcher.fetchmail()

        try:
            mails = fetcher.fetchmail()
        except Exception as ex:
            print(ex)

        for mail in mails:
            print(mail)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
