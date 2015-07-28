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

        fetcher = GMailFeedFetcher('user', 'password')
        fetcher.fetchmail()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
