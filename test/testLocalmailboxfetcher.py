#!/usr/bin/env python

from mailbox import NoSuchMailboxError
from testconstants import MBOX
import mailindicator.localmailboxfetcher
import os
import tempfile
import unittest

class TestLocalmailboxfetcher(unittest.TestCase):
    
    def testWrongPath(self):
        """Test for non existent mailbox"""
        mboxpath = '/unexistentfile'
        assert not os.path.exists(mboxpath)
        gotexception = False
        mboxfetcher = mailindicator.localmailboxfetcher.LocalMailboxFetcher(mboxpath)
        try:
            mboxfetcher.fetchmail()
        except NoSuchMailboxError, e:
            message = str(e)
            assert message == 'The specified mailbox does not exist /unexistentfile'
            gotexception = True
            
        assert gotexception
        
    def testNotReadable(self):
        """Test for non readable mailbox"""
        mboxpath = '/etc/shadow'
        gotexception = False
        mboxfetcher = mailindicator.localmailboxfetcher.LocalMailboxFetcher(mboxpath)
        try:
            mails = mboxfetcher.fetchmail()
        except Exception, e:
            message = str(e)
            #print message
            gotexception = True
            
        assert gotexception
        
    def testRead(self):
        tfile = tempfile.NamedTemporaryFile()
        tfile.write(MBOX)
        tfile.seek(0)
        mboxfetcher = mailindicator.localmailboxfetcher.LocalMailboxFetcher(tfile.name)
        mails = mboxfetcher.fetchmail()
        tfile.close()
        
        assert len(mails) == 1
        m = mails[0]        
        assert m.id == '<20121207074501.992D440418@testhost>'
        assert m.mfrom == 'testuser@testhost (Test User)'
        assert m.subject == 'This is a test subject'
        assert m.date == 'Fri,  7 Dec 2012 08:45:01 +0100 (CET)' 
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()