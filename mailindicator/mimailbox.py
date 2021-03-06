"""-"""
from mailindicator import gmailfeedfetcher, localmailboxfetcher, imapfetcher


class Mailbox:
    """Mailbox."""

    GMAILFEED = 'GMAILFEED'
    LOCALMBOX = 'LOCALMBOX'
    IMAP = 'IMAP'
    IMAPSTARTTLS = 'IMAPSTARTTLS'

    def __init__(self, typ, label, sleep_time, **kwargs):
        self.type = typ
        self.label = label
        self.sleep_time = int(sleep_time)
        if 'enabled' in kwargs:
            self.enabled = (kwargs['enabled'].lower() != 'false')
        else:
            self.enabled = True

        if self.type == Mailbox.GMAILFEED:
            self.fetcher = gmailfeedfetcher.GMailFeedFetcher(label, **kwargs)
        elif self.type == Mailbox.LOCALMBOX:
            self.fetcher = localmailboxfetcher.LocalMailboxFetcher(label, **kwargs)
        elif self.type == Mailbox.IMAP:
            self.fetcher = imapfetcher.ImapFetcher(label, **kwargs)
        else:
            raise Exception('Not a valid Mailbox type: %s' % typ)

    def get_attributes_to_store(self):
        """Return the list of attributes to save."""
        attributes = self.__dict__.copy()
        del attributes['type']
        del attributes['label']
        del attributes['fetcher']
        return attributes.items()
