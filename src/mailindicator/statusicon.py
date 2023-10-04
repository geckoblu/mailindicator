"""-"""
import threading
import gi
from gi.repository import GObject
from gi.repository import Gtk
gi.require_version('Notify', '0.7')
from gi.repository import Notify

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
        self.statusicon = Gtk.StatusIcon()
        self.statusicon.connect('popup-menu', self._right_click_event)
        self.statusicon.connect('activate', self._left_click_event)

        self.pynotify_available = Notify.init('mailindicator')
        self.monitors = []
        self.mailboxes = {}
        self.markedasread = {}
        self.notified = {}
        self.ignoreerrors = {}

        self.menu = None

    def set_monitors(self, monitors):
        """Set monitors"""
        self.monitors = monitors

    # def _show_preferences_dialog(self, widget):
    #    # TODO show preferences dialog
    #    pass

    def _refresh(self, widget):
        for monitor in self.monitors:
            monitor.refresh()

    def _left_click_event(self, icon):
        debug('StatusIcon clicked')
        # Thread safe
        self.lock.acquire()
        try:
            for label in list(self.mailboxes.keys()):
                mailbox = self.mailboxes[label]
                if not mailbox.inerror:
                    if label not in self.markedasread:
                        self.markedasread[label] = []
                    markedasread = self.markedasread[label]
                    markedasread = markedasread + mailbox.unread_ids
                    self.markedasread[label] = markedasread
                else:
                    if label not in self.ignoreerrors:
                        self.ignoreerrors[label] = []
                    ignoreerrors = self.ignoreerrors[label]
                    ignoreerrors += [mailbox.errormessage]
                    self.ignoreerrors[label] = ignoreerrors
                del self.mailboxes[label]
        finally:
            self.lock.release()

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
                tooltip_text = 'Error\n\n%s\n\n' % mb_errorsummary
            else:
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
            if inerror:
                GObject.idle_add(self.statusicon.set_from_icon_name, 'new-messages-red')
            elif newmail:
                GObject.idle_add(self.statusicon.set_from_icon_name, 'indicator-messages-new')
            else:
                # TODO 'set_from_stock' is just a trick to avoid to show an icon
                GObject.idle_add(self.statusicon.set_from_stock, 'indicator-messages')

            GObject.idle_add(self.statusicon.set_tooltip_text, tooltip_text)

        finally:
            self.lock.release()

    def set_mails(self, label, mails):
        """Set mails."""
        # Thread safe
        self.lock.acquire()
        try:
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
                                debug('StatusIcon %s: Mail not notified %s' % (label, mail))
                                notified.append(mail.id)
                                smr = smr.replace('<', '&lt;')
                                smr = smr.replace('>', '&gt;')
                                ntf = Notify.Notification.new('New Message', smr)
                                ntf.show()
                            else:
                                debug('StatusIcon %s: Mail already notified %s' % (label, mail))
                    else:
                        debug('StatusIcon %s: Mail marked as read %s' % (label, mail))

            if label in self.ignoreerrors:
                del self.ignoreerrors[label]

            if unread > 0:
                mailbox = MB(label)
                mailbox.unread = unread
                mailbox.unread_ids = unread_ids
                mailbox.summary = summary
                self.mailboxes[label] = mailbox
            else:
                info('StatusIcon %s: No unread mail found' % label)
                if label in self.mailboxes:
                    del self.mailboxes[label]
        finally:
            self.lock.release()

        self._update_status()

    def set_error(self, label, message):
        """Set error."""

        # Thread safe
        self.lock.acquire()
        try:
            if label in self.ignoreerrors and message in self.ignoreerrors[label]:
                return

            mailbox = MB(label)
            mailbox.inerror = True
            mailbox.errormessage = message
            self.mailboxes[label] = mailbox
        finally:
            self.lock.release()

        self._update_status()

    def _menu_item(self, icon_name, label):
        box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 6)
        icon = Gtk.Image()
        icon.set_from_icon_name(icon_name, Gtk.IconSize.MENU)
        label = Gtk.Label(label)

        box.add(icon)
        box.add(label)

        itm = Gtk.MenuItem()
        itm.add(box)

        return itm

    def _right_click_event(self, icon, button, time):
        debug('StatusIcon right click event')

        if self.menu is None:
            menu = Gtk.Menu()

            itm = self._menu_item('view-refresh', 'Refresh')
            itm.connect('activate', self._refresh)
            menu.append(itm)

            itm = Gtk.SeparatorMenuItem()
            menu.append(itm)

            # itm = self._menu_item('preferences-system', 'Preferences')
            # itm.connect('activate', self._show_preferences_dialog)
            # menu.append(itm)

            itm = self._menu_item('help-about', 'About')
            itm.connect('activate', self._show_about_dialog)
            menu.append(itm)

            itm = Gtk.SeparatorMenuItem()
            menu.append(itm)

            itm = self._menu_item('application-exit', 'Quit')
            itm.connect('activate', self._quit)
            menu.append(itm)
            menu.show_all()

            self.menu = menu

        self.menu.popup(None, None, None, None, button, time)

    def _show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_logo_icon_name(None)
        about_dialog.set_name('Mailindicator')
        about_dialog.set_version(VERSION)
        about_dialog.set_authors(['Alessio Piccoli <alepic@geckoblu.net>'])
        about_dialog.set_comments('Monitors your mailboxes for new mail')
        about_dialog.set_license(_LICENSE)
        about_dialog.set_copyright('Copyrigth (c) 2016')
        about_dialog.set_website('http://www.geckoblu.net/html/mailindicator.html')

        about_dialog.run()
        about_dialog.destroy()

    def _quit(self, widget):
        info('StatusIcon: Quitting')
        import sys
        sys.exit(0)


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
