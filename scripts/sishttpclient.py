#!/usr/bin/env python

import urllib, hashlib
import sys
filename = sys.argv[1]

## generate file hashes
h1 = hashlib.md5()
h2 = hashlib.sha1()
f = file(filename, 'rb')
while True:
	data = f.read(1024)
	if data == '':
		break
	h1.update(data)
	h2.update(data)
f.close()

hashstr = "MD5=%s;SHA1=%s" % (h1.hexdigest(), h2.hexdigest())
print hashstr

u = urllib.urlopen("http://devvm/sis/?" + urllib.urlencode({'action': 'sign', 'msg': hashstr}))
if u.code != 200:
	print "got " + str(u.code)
	sys.exit(1)
print u.read()
