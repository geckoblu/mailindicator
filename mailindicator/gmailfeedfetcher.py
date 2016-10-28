"""-"""
import base64
import feedparser

from mailindicator import Mail, AuthenticationError


class GMailFeedFetcher:
    """Fetch mails from GMail Feed"""

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
        """Fetch mails from GMail Feed"""

        credentials = base64.b64encode(bytes('%s:%s' % (self.username, self.passwd), 'utf-8'))

        url = 'https://mail.google.com/mail/feed/atom/'

        request_headers = {}
        request_headers['Authorization'] = b'Basic %s' % credentials

        try:
            feed = feedparser.parse(url, request_headers=request_headers)
            if feed.status == 401:
                raise AuthenticationError()
            elif feed.status >= 400:
                import BaseHTTPServer  # @UnresolvedImport : Just a problem with pydev, it is defined
                smsg, lmsg = BaseHTTPServer.BaseHTTPRequestHandler.responses[feed.status]
                raise Exception('HTTP ERROR %s - %s - %s' % (feed.status, smsg, lmsg))
        except AttributeError as ex:  # Raised by feed.status if something went wrong in parsing
            if feed.bozo == 1:
                raise feed.bozo_exception
            else:
                raise ex

        mails = []
        for entry in feed.entries:
            # print '-'*20
            # for key in entry.keys():
            #    print key, '\t\t', entry[key]
            # TODO for the date look at 'published_parsed'
            mail = Mail(entry['id'], entry['author'], entry['title'], entry['published'])
            mails.append(mail)

        return mails
