import pynotify


if __name__ == '__main__':
    pynotify.init('mailindicator')
    s = 'dojojojo'
    s = 'Mailbox: System\nFrom:        pippo@topolinia (Cron Daemon)\nSubject:    Cron <pdp@topolinia> ls -l\nSent:           Wed, 25 Jun 2014 09:28:01 +0200 (CEST)\n\n'
    s = 'Mailbox: System\nFrom:        pippo@topolinia (Cron Daemon)\nSubject:    Cron &lt;pdp&gt;'
    n = pynotify.Notification('New Message', s)
    n.show()
