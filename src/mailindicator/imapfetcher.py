"""-"""
from imaplib import IMAP4, IMAP4_SSL

from mailindicator import Mail


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

        self.security = None
        if 'security' in kwargs:
            security = kwargs['security'].upper()
            if security == 'NONE':
                self.security = None
            elif security == 'STARTTLS':
                self.security = 'STARTTLS'
            elif security == 'SSL/TLS':
                self.security = 'SSL/TLS'
            else:
                raise Exception('Wrong security parameter %s for : %s' % (security, label))

        if 'port' in kwargs:
            self.port = kwargs['port']
        else:
            if self.security == 'SSL/TLS':
                self.port = 993
            else:
                self.port = 143

    def fetchmail(self):
        """Fetch mails from IMAP"""
        mails = []

        if self.security == 'SSL/TLS':
            imap = IMAP4_SSL(self.host, self.port)
        else:
            imap = IMAP4(self.host, self.port)
            if self.security == 'STARTTLS':
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
