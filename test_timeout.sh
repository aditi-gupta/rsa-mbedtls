#!/bin/bash

address=$1

gdb -batch programs/pkey/rsa_sign \
	-ex 'set args "test.txt"' \
	-ex 'break main' \
	-ex 'run' \
	-ex 'print "breakpoint"' \
	-ex 'c'