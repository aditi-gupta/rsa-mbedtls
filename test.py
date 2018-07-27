#test
import subprocess

for i in range(0, 2):
	try:
		subprocess.call("./akda.sh", timeout=10)
		print (i)
	except subprocess.TimeoutExpired:
		print ("failed" + str(i))
	except FileNotFoundError:
		print ("failed " + str(i))