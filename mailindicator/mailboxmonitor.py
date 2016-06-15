"""-"""
import threading
import gobject
import mailindicator
from mailindicator.logging import info, debug, debug_ex
from mailindicator.network import network_available


class MailboxMonitor(threading.Thread):
    """Thread to monitor mailbox status."""

    def __init__(self, status_icon, label, sleep_time, fetchmail):
        threading.Thread.__init__(self)
        self.status_icon = status_icon
        self.label = label
        self.sleep_time = sleep_time * 1000  # Convert seconds in milliseconds
        self.fetchmail = fetchmail

    def run(self):
        """Overrides threading.Thread.run."""
        self._update()

    def _update(self):
        self.refresh()
        gobject.timeout_add(self.sleep_time, self._update)

    def refresh(self):
        """Refresh mailbox status."""

        info('MailboxMonitor %s: refresh.' % self.label)

        if network_available():
            # pylint: disable=broad-except
            try:
                mails = self.fetchmail()

                if len(mails) > 0:
                    debug('MailboxMonitor %s: %s Mail found' % (self.label, len(mails)))
                else:
                    debug('MailboxMonitor %s: No Mail found' % self.label)

                self.status_icon.set_mails(self.label, mails)
            except mailindicator.AuthenticationError as ex:
                message = 'Login failed, wrong user or password.'
                self.status_icon.set_error(self.label, message)
            except Exception as ex:
                debug_ex()
                message = 'Exception %s' % str(ex)
                self.status_icon.set_error(self.label, message)
        else:
            info('MailboxMonitor %s: Network not available' % self.label)
