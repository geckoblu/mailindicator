from mailbox import NoSuchMailboxError
from mailindicator import Mail
import mailbox

class LocalMailboxFetcher:
    
    def __init__(self, mboxpath):
        self.mboxpath = mboxpath

    def fetchmail(self):
        mails = []
        try:
            mbox = mailbox.mbox(self.mboxpath, create=False)
        except NoSuchMailboxError:
            raise NoSuchMailboxError('The specified mailbox does not exist %s' % self.mboxpath)
            
        items = mbox.items()
        for (key, message) in items:
            mail = Mail(message['Message-Id'], message['from'], message['subject'], message['Date'])
            mails.append(mail)
        
        return mails