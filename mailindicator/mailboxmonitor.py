from mailindicator.logging import debug, info
import gobject
import threading
import mailindicator


class MailboxMonitor(threading.Thread):
    def __init__(self, status_icon, label, sleep_time, fetchmail):
        threading.Thread.__init__(self)
        self.status_icon = status_icon
        self.label = label
        self.sleep_time = sleep_time * 1000 # Convert seconds in milliseconds
        self.fetchmail = fetchmail
        
        #self._update()
        
    def run(self):
        self._update()
        
    def refresh(self):
        debug('MailboxMonitor._update start')
        
        try:
            mails = self.fetchmail()
            
            if len(mails) > 0:
                debug('MailboxMonitor %s %s Mail found' % (self.label, len(mails)))
            else:
                debug('MailboxMonitor %s No Mail found' % self.label)
            
            self.status_icon.set_mails(self.label, mails)
        except mailindicator.AuthenticationError, e:
            message = 'Login failed, wrong user or password.'
            self.status_icon.set_error(self.label, message)
        except Exception, e:
            #TODO log the exception (stack trace)
            message = 'Exception %s' % str(e)
            self.status_icon.set_error(self.label, message)
        
    def _update(self):
        self.refresh()
        gobject.timeout_add(self.sleep_time, self._update)