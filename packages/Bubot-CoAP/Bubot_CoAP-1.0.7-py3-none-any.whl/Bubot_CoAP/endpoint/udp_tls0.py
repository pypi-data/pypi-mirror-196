from endpoint import UdpCoapEndpoint
import ssl
from dtls import do_patch
import socket

do_patch()


class UdpCoapsEndpoint(UdpCoapEndpoint):
    _scheme = 'coaps'
    ssl_transport = 1  # MBEDTLS_SSL_TRANSPORT_DATAGRAM = DTLS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.cert_filename = kwargs['certfile']
            self.key_filename = kwargs['keyfile']
        except KeyError as err:
            raise KeyError(f'{err} in CoapEndpoint not defined')

    @classmethod
    def init_unicast_ip4_by_address(cls, address, **kwargs):
        self = cls(**kwargs)
        self._multicast = None
        self._address = address
        self._family = socket.AF_INET
        _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._sock = ssl.wrap_socket(
            _sock,
            # keyfile=self.key_filename, certfile=self.cert_filename,
            # server_side=True, ssl_version=258
            # ciphers=['TLS_ECDH_ANON_WITH_AES_256_CBC_SHA']
            server_side=True, certfile=self.cert_filename,
            do_handshake_on_connect=False,
            ciphers="NULL"
        )
        self._sock.bind(address)
        return self

    @classmethod
    def init_unicast_ip6_by_address(cls, address, **kwargs):
        self = cls(**kwargs)
        self._multicast = None
        self._address = address
        self._family = socket.AF_INET6
        _sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        _sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock = ssl.wrap_socket(
            _sock,
            # keyfile=self.key_filename, certfile=self.cert_filename,
            server_side=True
        )
        self._sock.bind(address)
        return self

    # async def run(self, server, protocol_factory):
    #     # self.ssl_context = ssl.create_default_context()
    #     # self.ssl_context.load_cert_chain(certfile=self.cert_filename, keyfile=self.key_filename)
    #     self._transport, self._protocol = await server.loop.create_datagram_endpoint(
    #         lambda: protocol_factory(server, self), sock=self._sock)
    #     # self._transport = server.loop._make_ssl_transport(self._transport._sock, self._protocol, ssl_context, server_side=True)
    #     # await server.loop.start_tls(self._transport, self._protocol, ssl_context)

    pass
