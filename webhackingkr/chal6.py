import base64
import time
dat = "YzQwMzNiZmY5NGI1NjdhMTkwZTMzZmFhNTUxZjQxMWNhZWY0NDRmMg=="

while 1:
	dat = base64.decodestring(dat)
	print dat
	time.sleep(1)
