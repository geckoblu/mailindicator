VERSION = '0.1'


class Mail:
    def __init__(self, m_id, m_from, subject, date):
        self.id = m_id
        self.mfrom = m_from
        self.subject = subject
        self.date = date

    def __str__(self):
        return 'id: %s mfrom: %s subject: %s date: %s' % (self.id, self.mfrom, self.subject, self.date)


class AuthenticationError(Exception):
    """Authentication error.

    Most probably the server didn't accept the username/password
    combination provided.
    """
