import configparser
import os
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl

from mailindicator.sanction import Client, transport_headers

CLIENT_ID = '389343542305-2o2lhumlbomc29l6u5iucp9aoeue8pmi.apps.googleusercontent.com'
CLIENT_SECRET = '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'
TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
RESOURCE_ENDPOINT = 'https://mail.google.com'
SCOPE = 'https://mail.google.com/'
REDIRECT_URI = 'http://localhost:%s/login/google'

HTTP_SERVER_START_PORT = 8088
ENCODING_UTF8 = 'utf-8'


def get_HTTPServer():
    for port in range(HTTP_SERVER_START_PORT, HTTP_SERVER_START_PORT + 100):
        try:
            server = HTTPServer(('', port), _Handler)
            sys.stderr.write('Starting server on port %s \n' % port)
            return server
        except OSError:
            # sys.stderr.write('Already in use port %s \n' % port)
            pass


def _get_refresh_token_path():
    userhome = os.path.expanduser('~')
    xdg_state_home = os.environ.get('XDG_STATE_HOME') or \
        os.path.join(userhome, '.local', 'state')
    statedir = os.path.join(xdg_state_home, 'mailindicator')
    if not os.path.isdir(statedir):
        os.makedirs(statedir)
    return os.path.join(statedir, 'refresh_token')


def load_refresh_token(mailbox):
    config = configparser.ConfigParser()
    tokenpath = _get_refresh_token_path()
    if os.path.exists(tokenpath):
        try:
            with open(tokenpath, 'r') as configfile:
                config.read_file(configfile)
            tokens = config['tokens']
        except IOError as err:
            sys.stderr.write("WARNING: \"%s\" on opening %s\n" % (err.strerror, tokenpath))
            return None
        except KeyError as kerr:
            sys.stderr.write("WARNING: Missing section %s on config file %s\n" % (kerr, tokenpath))
            return None

        try:
            return tokens[mailbox]
        except KeyError as kerr:
            # Silently ignore this, this will request another token
            # TODO: log this?
            # sys.stderr.write("WARNING: Missing refresh token for '%s' on config file %s\n" % (mailbox, tokenpath))
            return None

    else:
        return None


def save_refresh_token(mailbox, refresh_token):
    config = configparser.ConfigParser()
    tokenpath = _get_refresh_token_path()

    if os.path.exists(tokenpath):
        try:
            with open(tokenpath, 'r') as configfile:
                config.read_file(configfile)
        except IOError:
            pass

        try:
            config['tokens']
        except KeyError:
            config.add_section('tokens')

    config.set('tokens', mailbox, refresh_token)

    with open(tokenpath, 'w') as configfile:
        config.write(configfile)


class GMailOAuth2:

    def __init__(self, mailbox):
        self.mailbox = mailbox

        self.server = None

    def read_feed(self):
        refresh_token = load_refresh_token(self.mailbox)
        if refresh_token:
            rc = Client(
                token_endpoint=TOKEN_ENDPOINT,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                resource_endpoint=RESOURCE_ENDPOINT,
                token_transport=transport_headers)

            rc.request_token(
                grant_type='refresh_token',
                refresh_token=refresh_token)

            return rc.request('/mail/feed/atom', parser=lambda c: c)

        else:
            data = self.request_new_token()
            return data

    def request_new_token(self):

        server = get_HTTPServer()
        server.mailbox = self.mailbox

        redirect_uri = REDIRECT_URI % server.server_port

        c = Client(
            auth_endpoint=AUTH_ENDPOINT,
            client_id=CLIENT_ID)

        auth_uri = c.auth_uri(
            login_hint=self.mailbox,
            scope=SCOPE,
            redirect_uri=redirect_uri,
            access_type='offline')

        # sys.stderr.write(auth_uri + '\n')
        webbrowser.open(auth_uri, new=2)

        # server.serve_forever()
        server.handle_request()
        
        return server.data


class _Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # self.log_message('>>>> ' + self.path)
        url = urlparse(self.path)
        qls = parse_qsl(url.query)

        # self.log_message(str(url))
        # self.log_message(str(qls))

        # sys.stderr.write(url.path + "\n")

        if url.path == '/login/google':
            self.handle_google_login(dict(qls))
        else:
            self.not_found()

    def not_found(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write('NOT FOUND'.encode(ENCODING_UTF8))
        # self.server_shutdown()

#    def server_shutdown(self):
#        x = threading.Thread(target=self.server.shutdown)
#        x.start()

    def handle_google_login(self, data):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if data.get('error'):
            errormessage = data.get('error')
            self.wfile.write(errormessage.encode(ENCODING_UTF8))
            # self.server_shutdown()

        else:
            c = Client(token_endpoint=TOKEN_ENDPOINT,
                resource_endpoint=RESOURCE_ENDPOINT,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_transport=transport_headers)

            redirect_uri = REDIRECT_URI % self.server.server_port

            c.request_token(code=data['code'],
                redirect_uri=redirect_uri)

            save_refresh_token(self.server.mailbox, c.refresh_token)
            
            self.wfile.write("AUTHENTICATION SUCCEEDED".encode(ENCODING_UTF8))
            
            self.server.data = c.request('/mail/feed/atom', parser=lambda c: c)
