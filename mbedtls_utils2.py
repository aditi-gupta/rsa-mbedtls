from fractions import gcd
import binascii
import os.path

def read_file(f):
	if os.path.isfile(f) == True:
		file = open(f, "r")
		x = "".join(file.read().split())
		file.close()
		x = int(x, 16)
		return x
	else:
		return "failed"

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

def read_pub_keys(file):
	keyfile = open(file, "r")
	lines = keyfile.readlines()
	n = int(lines[0].strip("N = "), 16)
	e = int(lines[1].strip("E = "), 16)
	return [n, e]

def solve_private_keys(e, s, m, n):
	p = gcd(pow(s, e)-m,n)
	q = n//p
	private_keys = [hex(p).strip("L"), hex(q).strip("L")]
	return private_keys

def decrypt(private_keys, e, n, c):
	p = int((private_keys[0].strip("0x")), 16)
	q = int((private_keys[1].strip("0x")), 16)
	totn = (p-1)*(q-1)
	d = modinv(e,totn)
	if not(d == None):
		decrypted = pow(c,d,n)
		return decrypted

def check_private_keys(correct_message, message):
	if correct_message == message:
		return "yes"

def read_memory(start, end):
	if os.path.isfile("gdb.txt") == True:
		f = open("gdb.txt", "r")
		current_data = ""
		for ln in f:
			for address in range(start, end, 16):
				if ln.startswith(str(hex(address))):
					count = 9
					while count<60:
						x = ln[count:count+11]
						new = str(x) + current_data
						current_data = new
						count += 11
		try:
			current_data = int("".join(current_data.replace("0x", "").split()), 16)
			return current_data
		except ValueError:
			return "failed to read memory"

def get_partial_sigs():
	s1 = read_memory(0x6f0280, 0x6f0300)
	s2 = read_memory(0x6f0310, 0x6f0390)
	if (type(s1) is int) and (type(s2) is int):
		return [hex(s1).strip("L"), hex(s2).strip("L")]