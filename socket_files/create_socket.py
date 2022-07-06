import socket
import contextlib


def _make_socket(iface_name: str, can_fd: bool) -> socket.SocketType:
    s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    try:
        s.bind((iface_name,))
        s.setsockopt(socket.SOL_SOCKET, 1, 1)  # timestamping
        if can_fd:
            s.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_FD_FRAMES, 1)

        s.setblocking(False)

        if 0 != s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR):
            raise OSError('Could not configure the socket: getsockopt(SOL_SOCKET, SO_ERROR) != 0')
    except BaseException:
        with contextlib.suppress(Exception):
            s.close()
        raise

    return s