"""-"""
import threading
import gobject
import gtk
import pynotify
from mailindicator import VERSION
from mailindicator.logging import debug, info


class MB:
    """MB"""
    def __init__(self, label):
        self.label = label
        self.inerror = False
        self.errormessage = ''
        self.unread = 0
        self.unread_ids = []
        self.summary = ''


class StatusIcon:
    """Status icon"""

    def __init__(self):
        self.lock = threading.Lock()
        self.statusicon = gtk.StatusIcon()
        self.statusicon.connect('popup-menu', self._right_click_event)
        self.statusicon.connect('activate', self._left_click_event)

        self.mailboxes = {}
        self.markedasread = {}
        self.notified = {}
        self.pynotify_available = pynotify.init('mailindicator')
        self.monitors = []

    def set_monitors(self, monitors):
        """Set monitors"""
        self.monitors = monitors

    def _show_preferences_dialog(self, widget):
        # TODO show preferences dialog
        pass

    def _refresh(self, widget):
        for monitor in self.monitors:
            monitor.refresh()

    def _left_click_event(self, icon):
        debug('StatusIcon clicked')
        for label in self.mailboxes.keys():
            mailbox = self.mailboxes[label]
            if not mailbox.inerror:

                if label not in self.markedasread:
                    self.markedasread[label] = []
                markedasread = self.markedasread[label]
                markedasread = markedasread + mailbox.unread_ids
                self.markedasread[label] = markedasread

                del self.mailboxes[label]

        self._update_status()

    def _update_status(self):
        # Thread safe
        self.lock.acquire()
        try:
            inerror = False
            newmail = False
            mb_summary = ''
            ms_summary = ''
            mb_errorsummary = ''
            for label in self.mailboxes.keys():
                mailbox = self.mailboxes[label]
                if mailbox.inerror:
                    inerror = True
                    mb_errorsummary = '%s%s : %s\n' % (mb_errorsummary,
                                                       mailbox.label,
                                                       mailbox.errormessage)
                else:
                    if mailbox.unread > 0:
                        newmail = True
                        mb_summary = '%s%s (%s)\n' % (mb_summary, mailbox.label, mailbox.unread)
                        ms_summary = '%s%s' % (ms_summary, mailbox.summary)

            # Update status icon
            if inerror:
                gobject.idle_add(self.statusicon.set_blinking, True)
                tooltip_text = 'Error\n\n%s\n\n' % mb_errorsummary
            else:
                gobject.idle_add(self.statusicon.set_blinking, False)
                tooltip_text = ''
            if newmail:
                ttxt = 'Mailboxes having new mail\n\n' + \
                       '%s\n\n' + \
                       'Mail summary\n\n%s'
                ttxt = ttxt % (mb_summary, ms_summary)
                tooltip_text = tooltip_text + ttxt
            else:
                if not inerror:
                    tooltip_text = 'No unread mails.'
            if newmail or inerror:
                gobject.idle_add(self.statusicon.set_from_icon_name, 'indicator-messages-new')
            else:
                # TODO 'set_from_stock' is just a trick to avoid to show an icon
                gobject.idle_add(self.statusicon.set_from_stock, 'indicator-messages')

            gobject.idle_add(self.statusicon.set_tooltip_text, tooltip_text)

        finally:
            self.lock.release()

    def set_mails(self, label, mails):
        """Set mails."""
        unread = 0
        if len(mails) > 0:

            if label not in self.markedasread:
                self.markedasread[label] = []
            markedasread = self.markedasread[label]

            unread_ids = []
            summary = ''
            for mail in mails:
                if mail.id not in markedasread:
                    unread += 1
                    unread_ids.append(mail.id)
                    if len(mail.subject) > 40:
                        mail.subject = mail.subject[0:40]
                    smr = 'Mailbox: %s\n' + \
                          'From:       %s\n' + \
                          'Subject:   %s\n' + \
                          'Sent:         %s\n\n'
                    smr = smr % (label, mail.mfrom, mail.subject, mail.date)
                    summary += smr

                    if self.pynotify_available:
                        if label not in self.notified:
                            self.notified[label] = []
                        notified = self.notified[label]

                        if mail.id not in notified:
                            debug('StatusIcon Mail not notified %s' % mail)
                            notified.append(mail.id)
                            smr = smr.replace('<', '&lt;')
                            smr = smr.replace('>', '&gt;')
                            ntf = pynotify.Notification('New Message', smr)
                            ntf.show()
                        else:
                            debug('StatusIcon Mail already notified %s' % mail)
                else:
                    debug('StatusIcon Mail marked as read %s' % mail)

        if unread > 0:
            mailbox = MB(label)
            mailbox.unread = unread
            mailbox.unread_ids = unread_ids
            mailbox.summary = summary
            self.mailboxes[label] = mailbox
        else:
            info('StatusIcon %s No unread mail found' % label)
            if label in self.mailboxes:
                del self.mailboxes[label]
        self._update_status()

    def set_error(self, label, message):
        """Set error."""
        mailbox = MB(label)
        mailbox.inerror = True
        mailbox.errormessage = message
        self.mailboxes[label] = mailbox

        self._update_status()

    def _right_click_event(self, icon, button, time):
        debug('StatusIcon right click event')
        menu = gtk.Menu()

        itm = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
        itm.connect("activate", self._refresh)
        menu.append(itm)

        itm = gtk.SeparatorMenuItem()
        menu.append(itm)

        itm = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        itm.connect("activate", self._show_preferences_dialog)
        menu.append(itm)

        itm = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        itm.connect("activate", self._show_about_dialog)
        menu.append(itm)

        menu.show_all()
        menu.popup(None, None, None, button, time)

    def _show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Mailindicator")
        about_dialog.set_version(VERSION)
        about_dialog.set_authors(["Alessio Piccoli <alepic@geckoblu.net>"])
        about_dialog.set_comments('Monitors your mailboxes for new mail')
        about_dialog.set_license(_LICENSE)
        about_dialog.set_copyright('Copyrigth (c) 2012')
        about_dialog.set_website('http://www.geckoblu.net/html/mailindicator.html')

        about_dialog.run()
        about_dialog.destroy()


_LICENSE = """This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA."""
