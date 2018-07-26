# before running this, you need to run chmod a+x gdb_readencrypted.sh and chmod a+x gdb_flip.sh

import csv
import mbedtls_utils2 as mu
import os
import subprocess

all_data = []

sigfile = "example.txt.sig"
keyfile = "rsa_pub.txt"
n = (mu.read_pub_keys(keyfile))[0]
e = (mu.read_pub_keys(keyfile))[1]

subprocess.call("./gdb_readencrypted.sh")
encrypted = mu.read_file("result-enc.txt")
correct_decrypted = mu.read_memory(0x6ea2b0, 0x6ea3b0)
os.remove("gdb.txt")

for i in range (0x40d27b, 0x40d41b): # (0x40d2a7, 0x40d2a8): 
	subprocess.call(["./gdb_flip.sh", str(i)])
	m = mu.read_memory(0x6f08a0, 0x6f09a0)
	i_data = {}
	i_data['Memory Address'] = hex(i)
	s = mu.read_file(sigfile)
	if not(s == "failed"):
		partials = mu.get_partial_sigs()
		i_data['Partial Signatures'] = partials
		os.remove("gdb.txt")
		pkeys = mu.solve_private_keys(e, s, m, n)
		i_data['Private Keys'] = pkeys
		os.remove(sigfile)
		decrypted = mu.decrypt(pkeys, e, n, encrypted)
		i_data['Correct?'] = mu.check_private_keys(correct_decrypted, decrypted)
	else:
		i_data['Private Keys'] = "failed"

	all_data.append(i_data)

print all_data

fields = ['Memory Address', 'Partial Signatures', 'Private Keys', 'Correct?']
with open('results_mbedtls_checked.csv', 'wb') as f:
    writer = csv.DictWriter(f, fieldnames = fields)
    writer.writeheader()
    writer.writerows(all_data)