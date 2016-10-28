import mailindicator.imapfetcher
import os
import unittest


class TestImapfetcher(unittest.TestCase):

    def testConnection(self):

        kwargs = {}
        try:
            kwargs['username'] = os.environ['username']
        except KeyError:
            raise Exception('Missing required username')

        try:
            kwargs['userpassword'] = os.environ['userpassword']
        except KeyError:
            raise Exception('Missing required userpassword')

        try:
            kwargs['host'] = os.environ['host']
        except KeyError:
            raise Exception('Missing required host')

        if 'port' in os.environ:
            kwargs['port'] = os.environ['port']

        if 'security' in os.environ:
            kwargs['security'] = os.environ['security']

        fetcher = mailindicator.imapfetcher.ImapFetcher('Test', **kwargs)

        # mails = fetcher.fetchmail()

        try:
            mails = fetcher.fetchmail()
            for mail in mails:
                print(mail)
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
