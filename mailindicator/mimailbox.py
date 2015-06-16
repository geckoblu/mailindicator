from mailindicator import gmailfeedfetcher, localmailboxfetcher, imapstarttlsfetcher


class Mailbox:
    GMAILFEED = 'GMAILFEED'
    LOCALMBOX = 'LOCALMBOX'
    IMAPSTARTTLS = 'IMAPSTARTTLS'

    def __init__(self, typ, label, sleep_time, **kwargs):
        self.type = typ
        self.label = label
        self.sleep_time = int(sleep_time)
        if kwargs.has_key('enabled'):
            self.enabled = (kwargs['enabled'].lower() != 'false')
        else:
            self.enabled = True

        if self.type == Mailbox.GMAILFEED:
            self.username = kwargs['username']
            self.userpassword = kwargs['userpassword']
            self.fetcher = gmailfeedfetcher.GMailFeedFetcher(self.username, self.userpassword)
        elif self.type == Mailbox.LOCALMBOX:
            self.mboxpath = kwargs['mboxpath']
            self.fetcher = localmailboxfetcher.LocalMailboxFetcher(self.mboxpath)
        elif self.type == Mailbox.IMAPSTARTTLS:
            self.username = kwargs['username']
            self.userpassword = kwargs['userpassword']
            self.host = kwargs['host']
            self.fetcher = imapstarttlsfetcher.ImapStartTlsFetcher(self.username, self.userpassword, self.host)
        else:
            raise Exception('Not a valid Mailbox type: %s' % typ)

    def get_attributes_to_store(self):
        attributes = self.__dict__.copy()
        del attributes['type']
        del attributes['label']
        del attributes['fetcher']
        return attributes.items()
