"""nssh.transport.socket"""
import logging
import socket
from typing import Optional

from nssh.exceptions import NSSHTimeout

LOG = logging.getLogger(f"nssh_transport")


class Socket:
    def __init__(self, host: str, port: int, timeout: int):
        self.host: str = host
        self.port: int = port
        self.timeout: int = timeout
        self.sock: Optional[socket.socket] = None

    def socket_open(self) -> None:
        """
        Open underlying socket

        Args:
            N/A  # noqa

        Returns:
            N/A  # noqa

        Raises:
            SetupTimeout: if socket connection times out

        """
        if not self.socket_isalive():
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            try:
                self.sock.connect((self.host, self.port))
            except socket.timeout:
                LOG.critical(f"Timed out trying to open socket to {self.host} on port {self.port}")
                raise NSSHTimeout(
                    f"Timed out trying to open socket to {self.host} on port {self.port}"
                )
            LOG.debug(f"Socket to host {self.host} opened")

    def socket_close(self) -> None:
        """
        Close socket

        Args:
            N/A  # noqa

        Returns:
            N/A  # noqa

        Raises:
            N/A  # noqa

        """
        if self.socket_isalive() and isinstance(self.sock, socket.socket):
            self.sock.close()
            LOG.debug(f"Socket to host {self.host} closed")

    def socket_isalive(self) -> bool:
        """
        Check if socket is alive

        Args:
            N/A  # noqa

        Returns:
            bool True/False if socket is alive

        Raises:
            N/A  # noqa

        """
        try:
            if isinstance(self.sock, socket.socket):
                self.sock.send(b"")
                return True
        except OSError:
            LOG.debug(f"Socket to host {self.host} is not alive")
            return False
        except AttributeError:
            LOG.debug(f"Socket to host {self.host} has never been created")
            return False
        return False