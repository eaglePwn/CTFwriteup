import struct
import subprocess

dat = ""
dat += struct.pack('<I',0x4b4f4f42) # file header
dat += "A"*32 # title
dat += "B"*256 # abstract
dat += struct.pack('<Q',0x0) # fptr
dat += struct.pack('<I',)
