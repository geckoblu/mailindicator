import feedparser

from mailindicator import Mail, AuthenticationError
from mailindicator.gmailoauth2 import GMailOAuth2


class GMailFeedFetcher:
    """Fetch mails from GMail Feed"""

    def __init__(self, label, **kwargs):
        try:
            self.mailbox = kwargs['mailbox']
        except KeyError:
            raise Exception('Missing required mailbox for : %s' % label)

    def fetchmail(self):

        gmailoauth2 = GMailOAuth2(self.mailbox)

        data = gmailoauth2.read_feed()

        if data:
            feed = feedparser.parse(data)
    
            mails = []
            for entry in feed.entries:
                # print '-'*20
                # for key in entry.keys():
                #    print key, '\t\t', entry[key]
                # TODO for the date look at 'published_parsed'
                mail = Mail(entry['id'], entry['author'], entry['title'], entry['published'])
                mails.append(mail)
    
            return mails


if __name__ == "__main__":
    feedfetcher = GMailFeedFetcher(label='GECKOBLU', mailbox='geckoblu01@gmail.com')
    feedfetcher.fetchmail()
