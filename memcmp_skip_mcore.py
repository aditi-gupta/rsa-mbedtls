# this is a manticore script to see what memory locations you can flip to skip over the memcmp check

from manticore import Manticore

for i in range(0x400b4c, 0x400b4d):
	m = Manticore('memcmp_skip_incorrect2')
	print hex(i)
	@m.hook(0x400b30)
	def hook(state):
		cpu = state.cpu
		location = cpu.read_int(i, 8)
		flipped = location ^ 1
		cpu.write_int(i, flipped, 8, force=True)

	@m.hook(0x400bfe)
	def hook2(state):
		cpu = state.cpu
		x = cpu.read_int(cpu.RBP-0x44)
		print hex(x)
	m.run(timeout = 30)


m = Manticore('memcmp_skip_correct')
print "correct"

@m.hook(0x400bfe)
def hook2(state):
	cpu = state.cpu
	x = cpu.read_int(cpu.RBP-0x44)
	print hex(x)
m.run(timeout = 30)