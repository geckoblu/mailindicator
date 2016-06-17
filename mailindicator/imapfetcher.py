"""-"""
from imaplib import IMAP4

from mailindicator import Mail, strtobool


class ImapFetcher:
    """Fetch mails from IMAP"""

    def __init__(self, label, **kwargs):

        try:
            self.username = kwargs['username']
        except KeyError:
            raise Exception('Missing required username for : %s' % label)

        try:
            self.passwd = kwargs['userpassword']
        except KeyError:
            raise Exception('Missing required userpassword for : %s' % label)

        try:
            self.host = kwargs['host']
        except KeyError:
            raise Exception('Missing required host for : %s' % label)

        if 'port' in kwargs:
            self.port = kwargs['port']
        else:
            self.port = 143

        self.starttls = 'starttls' in kwargs and strtobool(kwargs['starttls'])

    def fetchmail(self):
        """Fetch mails from IMAP"""
        mails = []

        imap = IMAP4(self.host, self.port)
        if self.starttls:
            imap.starttls()
        imap.login(self.username, self.passwd)
        imap.select(readonly=True)

        status, uids = imap.uid('SEARCH', 'UNSEEN')

        for uid in uids[0].split():
            status, data = imap.uid('FETCH', uid, '(BODY[HEADER.FIELDS (DATE SUBJECT FROM)])')
            message = self._message_from_data(data)
            mail = Mail(uid, message['FROM'], message['SUBJECT'], message['DATE'])
            mails.append(mail)

        imap.close()
        imap.logout()

        return mails

    def _message_from_data(self, data):
        body = data[0][1].decode('utf-8')
        message = {}
        for line in body.split('\n'):
            i = line.find(':')
            if i > -1:
                key = line[:i].strip().upper()
                value = line[i + 1:].strip()
                message[key] = value
        return message
