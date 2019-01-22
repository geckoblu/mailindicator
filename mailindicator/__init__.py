"""-"""
VERSION = '0.5.2'


class Mail:
    """Mail object."""
    def __init__(self, m_id, m_from, subject, date):
        self.id = m_id
        self.mfrom = m_from
        self.subject = subject
        self.date = date

    def __str__(self):
        return 'Mail[id:"%s", mfrom:"%s", subject:"%s", date:"%s"]' % \
                    (self.id,
                     self.mfrom,
                     self.subject,
                     self.date)

    def __repr__(self):
        return self.__str__()


class AuthenticationError(Exception):
    """Authentication error.

    Most probably the server didn't accept the username/password
    combination provided.
    """


def strtobool(val):
    """Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1';
    False is anything else.
    """
    val = val.lower()
    return val in ('y', 'yes', 't', 'true', 'on', '1')
