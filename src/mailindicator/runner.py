"""-"""
import argparse
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

import mailindicator.config as config
import mailindicator.logging as logging
from mailindicator.mailboxmonitor import MailboxMonitor
from mailindicator.statusicon import StatusIcon


def _parse_cmdline():

    parser = argparse.ArgumentParser(description='Monitors mailboxes for new mail.')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='show some debug messages in console')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='suppress non-error messages in console')
    parser.add_argument('-f', '--file',
                        type=argparse.FileType('r'),
                        help='use the given config file instead of the default one')

    return parser.parse_args()


def main():
    """Main function"""

    args = _parse_cmdline()

    if args.debug:
        logging.set_level(logging.DEBUG)
    elif args.quiet:
        logging.set_level(logging.NONE)
    else:
        logging.set_level(logging.INFO)

    if args.file:
        config.load(args.file)
    else:
        config.load()

    logging.info("Mailindicator started.")

    mailboxes = config.mailboxes
    monitors = []

    if len(mailboxes) > 0:
        status_icon = StatusIcon()

        for mailbox in mailboxes:
            mb_monitor = MailboxMonitor(status_icon,
                                        mailbox.label,
                                        mailbox.sleep_time,
                                        mailbox.fetcher.fetchmail)
            mb_monitor.start()
            monitors.append(mb_monitor)

        status_icon.set_monitors(monitors)

        Gdk.threads_init()
        Gtk.main()
    else:
        logging.info("No mailboxe configured. Exit.")
