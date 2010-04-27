# GPG=gpg
# GPGX=$(GPG) --no-default-keyring --secret-keyring ./gnupg/secring.gpg --keyring ./gnupg/pubring.gpg
GPG=gpg --homedir ./gnupg --lock-never --no-greeting

all:
	@echo boo

keygen-check:
	$(GPG) --dry-run --gen-key --batch keygen.txt

# keygen: keytrap
# 	passphrase=`dd if=/dev/urandom bs=1k count=1 |shasum |cut -d\  -f1`; \
# 	cat keygen.txt | sed -e 's/@PASSPHRASE@/$$passphase/' | $(GPG) --gen-key --batch; \
# 	fingerprint=`$(GPG) --list-keys --with-fingerprint --with-colons |grep -e '^fpr:' |head -1 |cut -d: -f10`; \
# 	echo "<?php \$$keyconfig = array('$$fingerprint', '$$passphrase');" >./gnupg/config.php
# 	$(MAKE) keyexport >./gnupg/publickey.asc
# 	$(MAKE) keylist

keygen: keytrap
	mkdir -p gnupg
	$(GPG) --rebuild-keydb-caches
	cat keygen.txt | $(GPG) --gen-key --batch; \
	fingerprint=`$(GPG) --list-keys --with-fingerprint --with-colons |grep -e '^fpr:' |head -1 |cut -d: -f10`; \
	#echo "<?php \$$keyconfig = array('$$fingerprint');" >./gnupg/config.php
	# $(MAKE) keyexport >./gnupg/publickey.asc
	$(MAKE) keylist

keylist:
	$(GPG) --list-keys --with-fingerprint
	$(GPG) --list-secret-keys --with-fingerprint

keyexport:
	@$(GPG) --export -a --no-comments --no-emit-version "Automated Signature Service" 

distclean:
	rm -rf gnupg

keytrap:
	[ ! -d "./gnupg" ]

# fixperms:
# 	chown -R www-data ./gnupg
# 	#chown www-data ./gnupg/*.gpg

