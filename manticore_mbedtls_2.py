import csv
from manticore import Manticore
from fractions import gcd
import binascii
import mbedtls_utils2 as mu

target = './programs/pkey/rsa_sign'
all_data = []

e = int("010001", 16)
n = int("AE1EC41FDD978C18CB43F9587F9B85DF804603100611497DCB445D157E44E717C78D53FAC3644DEA302645F6CFF852A785C3DAEA525BE01A4B1960D6512D97C677436ED17D03A55DDD8E41D737456C2B1512D533806EB048C5570269CBDFABB5E335821CE69C892A825A3896FC46990A8F6FECC759DAD9D6FD76BBF55BAA34B0789CACE898B6CC8CDBB50A0BFE7073A31DAF0B67845F76B71D42942B03FC02D6D68789C6CEF502C39AA0FB392E5E84BD1581E7295BDF6C45463FEA20A5220413381B82A72F95B1BB29AC6E833B70EB5B9F9D43B4D56A94ECBD02C1CBC8C8EED903485BD2A379A8B81B8FE20216EE6019A5F19656A483CCD9C23EB3B17678050B", 16)

for i in range(0x40d2a1, 0x40d2a3):
	i_data = {}
	i_data['Memory Address'] = hex(i)
	m = Manticore(target, ['example.txt'])
	
	@m.hook(0x4009ae) #the beginning of main
	def hook_flips(state):
		cpu = state.cpu
		mu.skip_checks(cpu)
		mu.bitflip(cpu, i)
	
	#if you want to read private signatures and stuff, do it here with a second hook at 0x40d30d
	#if you want to take the signature from memory, do it here with a third hook
	
	#to check whether it's actually created a signature
	@m.hook(0x400f73)
	def hook_check(state):
		executed = True
		#this doesn't really work but whatever

	m.run(timeout = 21600) #is this a good timeout length? when I ran it before, it took 5 hrs
	
	#if you want to take the signature from the .sig file, do it here
	if executed == True:
		s = mu.read_sig_file("example.txt.sig")
		pkeys = mu.solve_private_keys(e, s, message, n)
		i_data['Private Keys'] = pkeys
	else:
		i_data['Private Keys'] = "failed"

	all_data.append(i_data)

fields = ['Memory Address', 'Private Keys']
with open('results_mbedtls_d2a1d2a3.csv', 'wb') as f:
    writer = csv.DictWriter(f, fieldnames = fields)
    writer.writeheader()
    writer.writerows(all_data)