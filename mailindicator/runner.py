"""-"""
import argparse
import gtk
import mailindicator.logging as logging
from mailindicator.mailboxmonitor import MailboxMonitor
from mailindicator.statusicon import StatusIcon

import mailindicator.config as config


def _parse_cmdline():

    parser = argparse.ArgumentParser(description='Monitors mailboxes for new mail.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='show some debug messages in console')
    parser.add_argument('-q', '--quiet',
                        dest='quiet',
                        action='store_true',
                        help='suppress non-error messages in console')

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

    logging.set_level(logging.DEBUG)

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

        gtk.gdk.threads_init()  # @UndefinedVariable : Just a problem with pydev, it is defined
        gtk.main()
