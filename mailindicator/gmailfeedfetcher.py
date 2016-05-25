import base64
import feedparser
from mailindicator import Mail
import mailindicator


class GMailFeedFetcher:

    def __init__(self, label, **kwargs):
        try:
            self.username = kwargs['username']
        except KeyError:
            raise Exception('Missing required username for : %s' % label)

        try:
            self.passwd = kwargs['userpassword']
        except KeyError:
            raise Exception('Missing required userpassword for : %s' % label)

    def fetchmail(self):

        credentials = base64.b64encode('%s:%s' % (self.username, self.passwd))

        url = 'https://mail.google.com/mail/feed/atom/'

        request_headers = {}
        request_headers['Authorization'] = 'Basic %s' % credentials

        try:
            d = feedparser.parse(url, request_headers=request_headers)
            if d.status == 401:
                raise mailindicator.AuthenticationError()
            elif d.status >= 400:
                import BaseHTTPServer
                smsg, lmsg = BaseHTTPServer.BaseHTTPRequestHandler.responses[d.status]
                raise Exception('HTTP ERROR %s - %s - %s' % (d.status, smsg, lmsg))
        except AttributeError as e:  # Raised by d.status if something went wrong in parsing
            if d.bozo == 1:
                raise d.bozo_exception
            else:
                raise e

        mails = []
        for entry in d.entries:
            # print '-'*20
            # for key in entry.keys():
            #    print key, '\t\t', entry[key]
            # TODO for the date look at 'published_parsed'
            mail = Mail(entry['id'], entry['author'], entry['title'], entry['published'])
            mails.append(mail)

        return mails
