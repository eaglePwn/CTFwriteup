import socket
import struct
from hexdump import *
s = socket.create_connection(['vortex.labs.overthewire.org',5842])

i = 0
i += struct.unpack("<I",s.recv(4))[0] 
i += struct.unpack("<I",s.recv(4))[0]
i += struct.unpack("<I",s.recv(4))[0]
i += struct.unpack("<I",s.recv(4))[0]

s.send(struct.pack("<I",i))

print [s.recv(1025)]
