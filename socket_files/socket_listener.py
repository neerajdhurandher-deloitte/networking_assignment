import socket
import struct


def addListener(self, addr, port, service):
    if self.isBroadcast(addr):
        self.etherAddrs[addr] = self.broadcastIpToMac(addr)
    elif self.isMulticast(addr):
        self.etherAddrs[addr] = self.multicastIpToMac(addr)
    else:
        # unicast -- we don't know yet which IP we'll want to send to
        self.etherAddrs[addr] = None

    # Set up the receiving socket and corresponding IP and interface information.
    # One receiving socket is required per multicast address.
    rx = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    for interface in self.interfaces:
        (ifname, mac, ip, netmask) = self.getInterface(interface)

        # Add this interface to the receiving socket's list.
        if self.isBroadcast(addr):
            rx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        elif self.isMulticast(addr):
            packedAddress = struct.pack('4s4s', socket.inet_aton(addr), socket.inet_aton(ip))
            rx.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, packedAddress)

        # Generate a transmitter socket. Each interface
        # requires its own transmitting socket.
        if interface not in self.noTransmitInterfaces:
            tx = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
            tx.bind((ifname, 0))

            self.transmitters.append(
                {'relay': {'addr': addr, 'port': port}, 'interface': ifname, 'addr': ip, 'mac': mac, 'netmask': netmask,
                 'socket': tx, 'service': service})

    rx.bind((addr, port))
    self.receivers.append(rx)