#!/bin/bash

gdb -batch programs/pkey/rsa_encrypt \
	-ex 'set args "key_check.txt"' \
	-ex 'set logging on' \
	-ex 'break *0x40ada7' \
	-ex 'run' \
	-ex 'x /64x 0x6ea2b0' \
	-ex 'c'