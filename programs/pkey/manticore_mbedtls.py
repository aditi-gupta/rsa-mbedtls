import csv
from manticore import Manticore
from fractions import gcd
import binascii

'''
target is rsa_sign.c (no need for rsa.c because rsa_sign.c calls the function from rsa.c that you want)
use mcore to go into rsa_sign.c file and flip a bit in the area you want (within the function mbedtls_rsa_private)
then continue through rsa_sign.c to finish signing the message and extract data from rsa_sign.c
try to use that data to get the private keys back!

for now: try to go into rsa_sign.c, give it input, and get out the signature
then, get manticore to flip a bit
next steps will be to get out the partials and try to decrypt, but that's way in the future for now
'''

target = './programs/pkey/rsa_sign example.txt'
m_correct = Manticore(target)
# m_correct.verbosity(2)
@m_correct.hook(0xc73a) #the end of the section of the mbedtls_rsa_private function where the decrypted message is outputed

def hook(state):
	cpu = state.cpu
	print 0xc73a
	sig = cpu.read_int(cpu.RBX)
	print sig

# question: in a manticore script, where would you specify the argv (the file you want to sign)?

m_correct.run()