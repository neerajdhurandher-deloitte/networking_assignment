import encodings
import socket
from datetime import date


def get_package_header():
    ethernet_mac = bytearray([0x7C, 0x70, 0xDB, 0x3B, 0xC6, 0xAE])
    ethernet_datatype = bytearray([0x08, 0x00])
    ip = bytearray("0" * 20, encodings.normalize_encoding("utf-8"))
    udp_port = bytearray([0x27, 0x10, 0x23, 0x68])
    udp_length = bytearray([0x00])
    udp_checkSum = bytearray([0x00])
    return ethernet_mac + ethernet_datatype + ip + udp_port + udp_length + udp_checkSum


def get_package_structure(msg: str, sig: str):
    st_pack = bytearray([0xEE, 0xFF])
    model = bytearray([0x01, 0x02, 0x03, 0x04])
    reserved1 = bytearray([0x00] * 20)
    byte26_32 = bytearray([0xAA, 0xBB, 0xCC, 0xDD, 0xFF, 0xAB, 0xAC])
    reserved2 = bytearray([0x00] * 25)
    begin_data1 = bytearray([0xFE, 0xEF])
    msg_data = bytearray(msg, encodings.normalize_encoding("utf-8"))
    assert len(msg_data) <= 36
    msg_data += bytearray([0x00] * (36-len(msg_data)))
    crc1 = bytearray([0x1, 0x0, 0x0, 0x1])
    begin_data2 = bytearray([0xAF, 0xFA])
    data2 = bytearray([0x00] * 48)
    crc2 = bytearray([0x1, 0x0, 0x0, 0x1])
    present_day = date.today().timetuple()
    age_data = bytearray([present_day.tm_year - 1900, present_day.tm_mon, present_day.tm_hour, present_day.tm_min,
                          present_day.tm_sec])

    time_stamp = bytearray((present_day.tm_hour * 60*60 + present_day.tm_min*60 + present_day.tm_sec) * (10**6))
    upd_seq = bytearray()
    sig_data = bytearray(sig, encodings.normalize_encoding("utf-8"))
    res = st_pack + model + reserved1 + byte26_32 + reserved2 + begin_data1 + msg_data + crc1
    res += begin_data2 + data2 + crc2 + age_data + time_stamp + upd_seq + sig_data
    return res

while True:
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(get_package_header() + get_package_structure("hello", "hhh"), (UDP_IP, UDP_PORT))