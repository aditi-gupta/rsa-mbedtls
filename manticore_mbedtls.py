import csv
from manticore import Manticore
from fractions import gcd
import binascii

target = './programs/pkey/rsa_sign'
m = Manticore(target, ['example.txt'])
m.verbosity(2)
print "start"

@m.hook(0x40d27b)
def hook(state):
	print "hook"
	# cpu = state.cpu
	# message = cpu.read_int(0x6f08a0)
	# print message

	# sig = cpu.read_int(cpu.RBP-0x15c)
	# print sig

m.run()
print "end"
