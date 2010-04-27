#!/usr/bin/env python

import gnupg
g = gnupg.GPG(gnupghome="../gnupg")

key = g.list_keys(secret=True)[0]
sig = g.sign('hello', keyid=key['fingerprint'])
print g.export_keys(key['fingerprint'])

# sig = g.sign('hello')
print sig