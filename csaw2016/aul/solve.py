import socket

def recvu(conn,string):
	r = ""
	while not r.endswith(string):
		tmp = conn.recv(1)
		if not tmp:break
		r += tmp
	return r
conn = socket.create_connection(['pwn.chal.csaw.io',8001])

print [conn.recv(1024)]
print [conn.recv(1024)]
conn.send('help\n')
print recvu(conn,'help')
f = open('help','w')
r = recvu(conn,'Didn')[2:-4]
f.write('\x1b')
f.write(r)
f.close
