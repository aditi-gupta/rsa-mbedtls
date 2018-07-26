from manticore import Manticore

for i in range(0x400b76, 0x400bc5):
	m = Manticore('glitching_skip_incorrect')
	print hex(i)
	@m.hook(0x400b60)
	def hook(state):
		cpu = state.cpu
		location = cpu.read_int(i, 8)
		flipped = location ^ 1
		cpu.write_int(i, flipped, 8, force=True)

	@m.hook(0x400bb3)
	def hook2(state):
		cpu = state.cpu
		x = cpu.read_int(cpu.RBP-0x10)
		print hex(x)
	m.run(timeout = 30)


# m2 = Manticore('glitching_skip_correct')
# print "correct!"

# @m2.hook(0x400bb3)
# def hook2(state):
# 	cpu = state.cpu
# 	x = cpu.read_int(cpu.RBP-0x10)
# 	print hex(x)
# m2.run(timeout = 30)


# for i in range(0x400b8a, 0x400b8b):
	# m2 = Manticore('glitching_skip_correct')
	# print hex(i)
	# @m2.hook(0x400b60)
	# def hook(state):
	# 	cpu = state.cpu
	# 	location = cpu.read_int(i, 8)
	# 	flipped = location ^ 1
	# 	cpu.write_int(i, flipped, 8, force=True)

	# @m2.hook(0x400bb3)
	# def hook2(state):
	# 	cpu = state.cpu
	# 	x = cpu.read_int(cpu.RBP-0x10)
	# 	print hex(x)
	# m2.run(timeout = 30)
