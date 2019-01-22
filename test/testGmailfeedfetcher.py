from mailindicator.gmailfeedfetcher import GMailFeedFetcher
import os
import unittest


class TestGmailfeedfetcher(unittest.TestCase):

    def testConnection(self):
        import mailindicator.config as config
        config.load()

        try:
            username = os.environ['username']
        except KeyError:
            raise Exception('Missing required username')
        try:
            userpassword = os.environ['userpassword']
        except KeyError:
            raise Exception('Missing required userpassword')

        fetcher = GMailFeedFetcher('GMAIL', username=username, userpassword=userpassword)
        mails = fetcher.fetchmail()
        print(mails)
        #print("["+", ".join(mails)+"]")


if __name__ == "__main__":
    unittest.main()
