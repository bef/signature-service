#!/usr/bin/env python
##
## SIS Signature Service
## proof of concept implementation for protocol version 1
## 26 April 2010
## Ben Fuhrmannek <ben@fuhrmannek.de>
## 

from SocketServer import UnixStreamServer, StreamRequestHandler
import os, sys
import gnupg
import datetime

PROTO_VERSION_STRING = "1" ## protocol version
VERSION_STRING = "0.1" ## program version
HELP_STRING = "SIS Signature Service Daemon v" + VERSION_STRING

## parse opts
def parse_opts():
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-s", "--socket", dest="socket", default="/tmp/sis.sock")
	parser.add_option("-k", "--secret-key", dest="fingerprint", default=None)
	return parser.parse_args()

(opts, args) = parse_opts()

#print opts, args

## init gnupg and select secret key
g = gnupg.GPG(gnupghome="../gnupg")
if opts.fingerprint:
	if not opts.fingerprint in g.list_keys(secret=True).fingerprints:
		print "error: fingerprint not in secret keyring"
		sys.exit(1)
else:
	opts.fingerprint = g.list_keys(secret=True).fingerprints[0]


## request handler
class SISRequestHandler(StreamRequestHandler):
	def handle(self):
		print "connection."
		while True:
			l = self.rfile.readline()
			if l == "":
				break ## end of connection
			l = l.strip()
			print l
			
			if l == 'HELP':
				self.reply(HELP_STRING)
			elif l == 'VERSION':
				self.reply(PROTO_VERSION_STRING)
			elif l == 'MULTILINETEST':
				self.reply_multiline("lorem ipsum\ndolor sit amet")
			elif l == 'EXPORTKEY':
				msg = str(g.export_keys(opts.fingerprint))
				self.reply_multiline(msg)
			elif l[:4] == 'SIGN' and len(l) > 5:
				sig = g.sign(datetime.datetime.today().isoformat() + "\n" + l[5:], keyid=opts.fingerprint)
				self.reply_multiline(str(sig))
			else:
				self.reply("go away.", "404")
			
	def reply(self, line, code="200"):
		self.wfile.write(code + " " + line + "\n")
	
	def reply_multiline(self, data):
		self.wfile.write("200 READ=" + str(len(data)) + "\n")
		self.wfile.write(data)
		self.wfile.flush()

## print status information
print HELP_STRING
print "Protocol Version", PROTO_VERSION_STRING

## start server
try:
	os.remove(opts.socket)
except OSError:
	pass

s = UnixStreamServer(opts.socket, SISRequestHandler)
os.chmod(opts.socket, 0777)
s.serve_forever()

