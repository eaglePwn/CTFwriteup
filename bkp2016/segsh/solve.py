import socket
import telnetlib
import struct

def recv_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r
s = socket.create_connection(['0',1234])
print [s.recv(1024)]

print "****interact****"
t = telnetlib.Telnet()
t.sock = s
t.interact()
