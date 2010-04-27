#!/usr/bin/env python
##
## interactive sis client
##

import socket, re
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/sis.sock")
f = s.makefile()
while True:
	i = raw_input("> ")
	s.send(i.strip() + "\n")
	r = f.readline().strip()
	mo = re.match('200 READ=(\d+)', r)
	if mo:
		size = int(mo.group(1))
		print "reading " + str(size) + " bytes"
		print f.read(size)
	else:
		print r
