from logging import info, debug
from mailindicator.mailboxmonitor import MailboxMonitor
from mailindicator.statusicon import StatusIcon
import argparse
import mailindicator.config as config
import gtk
import logging
import os

def parse_cmdline():
    
    def directory(repo):
        repoDir = os.path.abspath(os.path.expanduser(repo))
        if not os.path.isdir(repoDir):
            msg = '%r is not a directory' % repo
            raise argparse.ArgumentTypeError(msg)
        return repoDir
    
    parser = argparse.ArgumentParser(description='Monitors mailboxes for new mail.')
    parser.add_argument('--debug', action='store_true', help='show some debug messages in console')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='suppress non-error messages in console')
    
    return parser.parse_args()

def error(message):
    #TODO show error in a popup dialog
    logging.error(message)

def main():
    
    args = parse_cmdline()
    
    if args.debug:
        logging.setLevel(logging.DEBUG)
    elif args.quiet:
        logging.setLevel(logging.NONE)
    else:
        logging.setLevel(logging.INFO)
        
    logging.setLevel(logging.DEBUG)
        
    config.load()
    
    info("Mailindicator started.")
    
    mailboxes = config.mailboxes
    monitors = []
    
    if len(mailboxes) > 0:    
        status_icon = StatusIcon()
        
        for mailbox in mailboxes:
            mb_monitor = MailboxMonitor(status_icon, mailbox.label, mailbox.sleep_time, mailbox.fetcher.fetchmail)
            mb_monitor.start()
            monitors.append(mb_monitor)

        status_icon.set_monitors(monitors)
                
        gtk.gdk.threads_init() #@UndefinedVariable : Just a problem with pydev, it is defined
        gtk.main()
