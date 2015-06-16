from imaplib import IMAP4_PORT, IMAP4, Commands, __all__
import ssl


Commands['STARTTLS'] = ('NONAUTH',)


class IMAP4_STARTTLS(IMAP4):

    """IMAP4 client class over SSL connection

    Instantiate with: IMAP4_SSL([host[, port[, keyfile[, certfile]]]])

            host - host's name (default: localhost);
            port - port number (default: standard IMAP4 SSL port).
            keyfile - PEM formatted file that contains your private key (default: None);
            certfile - PEM formatted certificate chain file (default: None);

    for more documentation see the docstring of the parent class IMAP4.
    """

    def __init__(self, host='', port=IMAP4_PORT, keyfile=None, certfile=None):
        self._tls_established = False
        self.keyfile = keyfile
        self.certfile = certfile
        IMAP4.__init__(self, host, port)
        self.starttls()

#        def open(self, host = '', port = IMAP4_PORT):
#            """Setup connection to remote server on "host:port".
#                (default: localhost:standard IMAP4 SSL port).
#            This connection will be used by the routines:
#                read, readline, send, shutdown.
#            """
#            self.host = host
#            self.port = port
#            self.sock = socket.create_connection((host, port))
#            self.sslobj = ssl.wrap_socket(self.sock, self.keyfile, self.certfile)
#            self.file = self.sslobj.makefile('rb')

    def starttls(self, ssl_context=None):
        name = 'STARTTLS'
        if self._tls_established:
            raise self.abort('TLS session already established')
        if name not in self.capabilities:
            raise self.abort('TLS not supported by server')
        # Generate a default SSL context if none was passed.
#        if ssl_context is None:
#            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#            # SSLv2 considered harmful.
#            ssl_context.options |= ssl.OP_NO_SSLv2
        typ, dat = self._simple_command(name)
        if typ == 'OK':
            # self.sock = socket.create_connection((self.host, self.port))
            self.sslobj = ssl.wrap_socket(self.sock, self.keyfile, self.certfile)
            self.file = self.sslobj.makefile('rb')
            self._tls_established = True
            self._get_capabilities()
        else:
            raise self.error("Couldn't establish TLS session")
        return self._untagged_response(typ, dat, name)

    def _get_capabilities(self):
        typ, dat = self.capability()
        if dat == [None]:
            raise self.error('no CAPABILITY response from server')
        self.capabilities = tuple(dat[-1].upper().split())

    def read(self, size):
        """Read 'size' bytes from remote."""
        return self.file.read(size)

    def readline(self):
        """Read line from remote."""
        return self.file.readline()

    def send(self, data):
        """Send data to remote."""
        if self._tls_established:
            bytes = len(data)
            while bytes > 0:
                sent = self.sslobj.write(data)
                if sent == bytes:
                    break  # avoid copy
                data = data[sent:]
                bytes = bytes - sent
        else:
            self.sock.sendall(data)

    def shutdown(self):
        """Close I/O established in "open"."""
        self.file.close()
        self.sock.close()

    def socket(self):
        """Return socket instance used to connect to IMAP4 server.

        socket = <instance>.socket()
        """
        return self.sock

    def ssl(self):
        """Return SSLObject instance used to communicate with the IMAP4 server.

        ssl = ssl.wrap_socket(<instance>.socket)
        """
        return self.sslobj

    __all__.append("IMAP4_SSL")
