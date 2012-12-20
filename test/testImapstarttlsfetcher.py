import mailindicator.imapstarttlsfetcher
import unittest


class TestImapstarttlsfetcher(unittest.TestCase):


    def testConnection(self):
        HOST = 'mercurio.it.wuerth.com'
        USERNAME = 'b02183'
        PASSWORD = 'Leonida78'
        
        class error(Exception):
            pass
        
        e = error('ciao')
        
        fetcher = mailindicator.imapstarttlsfetcher.ImapStartTlsFetcher(USERNAME, PASSWORD, HOST)
        
        #_, mails = fetcher.fetchmail()
        
        try:
            _, mails = fetcher.fetchmail()
        except Exception, e:
            print e
        
#        for mail in mails:
#            print mail


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()