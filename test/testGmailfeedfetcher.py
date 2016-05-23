from mailindicator.gmailfeedfetcher import GMailFeedFetcher
import os
import unittest


class TestGmailfeedfetcher(unittest.TestCase):

    def testConnection(self):
        print os.environ
        del os.environ['http_proxy']
        del os.environ['https_proxy']
        print os.environ

        import mailindicator.config as config
        config.load()

        os.environ['https_proxy'] = 'http://127.0.0.1:6060'

        try:
            username = os.environ['username']
        except KeyError:
            raise Exception('Missing required username')
        try:
            userpassword = os.environ['userpassword']
        except KeyError:
            raise Exception('Missing required userpassword')

        fetcher = GMailFeedFetcher('GMAIL', username=username, userpassword=userpassword)
        fetcher.fetchmail()


if __name__ == "__main__":
    unittest.main()
