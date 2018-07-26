from fractions import gcd
import binascii

def skip_checks(cpu):
	a = cpu.read_int(0x40b9bb, 8)
	flipped_a = a ^ 1
	cpu.write_int(a, flipped_a, 8, force=True)
	b = cpu.read_int(0x406bdb, 8)
	flipped_b = b ^ 0x10
	cpu.write_int(b, flipped_b, 8, force=True)

#this isn't going to work - you have to use mcore to figure out how best to read these numbers
def get_partial_sigs(cpu):
	#s1
	for l in range(0x6df4e0, 0x6df560):
		x = cpu.read_bytes(l, 4)
	#s2
	for m in range(0x6e1b00, 0x6e1b80):
		y = cpu.read_bytes(m, 4)

	return [s1, s2]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		return None
	else:
		return x % m

# def get_private_keys(cpu):
# 	p = cpu.read_int(cpu.RBP-0x18)
# 	q = cpu.read_int(cpu.RBP-0x20)
# 	return p, q

# def get_public(cpu):
# 	e = cpu.read_int(cpu.RBP-0x38)
# 	n = cpu.read_int(cpu.RBP-0x28)
# 	m = cpu.read_int(cpu.RBP-0x10)
# 	s = cpu.read_int(cpu.RBP-0x80)
# 	return e, n, m, s

def solve_private_keys(e, s, m, n):
	p = gcd(pow(s, e)-m,n)
	q = n//p
	private_keys = [hex(p), hex(q)]
	return private_keys

# def decrypt(p, q, e, s, m, n, flag):
# 	totn = (p-1)*(q-1)
#     d = modinv(e,totn)
#     flag = pow(int(flag,16),d,n)
#     flag = hex(flag)
#     flag = flag.rstrip("L")[2:]
#     if(len(flag) % 2 == 1):
#         flag = '0'+ flag
#     return binascii.unhexlify(flag)

def decrypt(p, q, e, s, m, n, flag):
	totn = (p-1)*(q-1)
	d = modinv(e,totn)
	if not(d == None):
		decrypted = pow(flag,d,n)
		return decrypted

def bitflip(cpu, memory_location):
	location = cpu.read_int(memory_location, 8)
	flipped = location ^ 1
	cpu.write_int(memory_location, flipped, 8, force=True)

# def check_private_keys_keys(correct_keys, keys):
# 	if set(keys) == set(correct_keys):
# 		return "yes"

def check_private_keys_message(correct_message, message):
	if correct_message == message:
		return "yes"
