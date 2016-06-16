"""-"""
from mailbox import NoSuchMailboxError
import mailbox

from mailindicator import Mail


class LocalMailboxFetcher:
    """Fetch mails from local mailbox"""

    def __init__(self, label, **kwargs):
        try:
            self.mboxpath = kwargs['mboxpath']
        except KeyError:
            raise Exception('Missing required mboxpath for : %s' % label)

    def fetchmail(self):
        """Fetch mails from local mailbox"""
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
