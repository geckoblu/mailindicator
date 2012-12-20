import base64
import urllib2
import feedparser
from mailindicator import Mail
import mailindicator

USER_AGENT = 'User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)'

class GMailFeedFetcher:
    
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def fetchmail(self):
        
        credentials = base64.encodestring('%s:%s' % (self.user, self.passwd))
        
        url = 'https://mail.google.com/mail/feed/atom/'
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Authorization', 'Basic %s' % credentials)
        
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise mailindicator.AuthenticationError(e)
            else:
                raise e
        
        pageData = resp.read()
        
        mails = []
        
        d = feedparser.parse(pageData)
        for entry in d.entries:
            #print '-'*20
            #for key in entry.keys():
            #    print key, '\t\t', entry[key]
            # TODO for the date look at 'published_parsed'
            mail = Mail(entry['id'], entry['author'], entry['title'], entry['published'])
            mails.append(mail)
            
        return mails