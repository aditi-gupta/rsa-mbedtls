#!/bin/bash

address=$1

gdb -batch programs/pkey/rsa_sign \
	-ex 'set args "example.txt"' \
	-ex 'set logging on' \
	-ex 'break main' \
	-ex 'break *0x40d27b' \
	-ex 'break *0x40d30d' \
	-ex 'run' \
	-ex 'set *'$address' ^= 0x1' \
	-ex 'set *0x40b7f4 ^= 0x1' \
	-ex 'set *0x40d4f6 ^= 0x10' \
	-ex 'c' \
	-ex 'x /64x 0x6f08a0' \
	-ex 'c' \
	-ex 'x /32x 0x6f0280' \
	-ex 'x /32x 0x6f0310' \
	-ex 'c'