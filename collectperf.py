#!/usr/bin/python
import getpass
import os
import subprocess
import threading
import time
import sys

def login():
    user = raw_input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()
    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))
    p1, p2 = pprompt()
    while p1 != p2:
        print('Passwords do not match. Try again')
        p1, p2 = pprompt()
    return user, p1


hosts = []
resxtop = "/usr/bin/resxtop"
esxtopconfig = """abcdefghij
abcdefghijklmnopq
AbcdEfGhijkl
abcdefghijklmnop
abcdefgh
abcdefghijklmno
abcdef
abcde
9d
"""


print "Checking for prerequisite hosts file esxhosts:",
if (not os.path.isfile("esxhosts")):
	exit("esxhosts file does not exist")
else:
	print "found!"
print "Reading file esxhosts"
for line in open('esxhosts'):
	if (len(line) > 2):
		hosts.append(line.strip())
print "Entries: " + str(len(hosts))

vcenterhost = raw_input("Enter vCenter Hostname/IP: ")
print "Enter vCenter Credentials"
username,password = login()


print """Please select a number of minutes to collect data (collects data every 60s):
1 day = 1440 (minutes)
"""


collectioninterval = int(raw_input("Enter collection iterations: "))
comeback = round((float(collectioninterval) * 1) / 60,2)


print "Writing esxtop config"
f = open('.esxtop50rc','w')
f.write(esxtopconfig)
f.close()

print "Saving session file..."
p = subprocess.call(["/usr/lib/vmware-vcli/apps/session/save_session.pl","--username",username,"--server",vcenterhost,"--password",password,"--savesessionfile",".sessionfile"])

my_env["VI_SESSIONFILE"] = "./.sessionfile"
print "Collecting scsi device data for correlation..."
for hostname in hosts:
	print "Collecting for " + hostname
	p = subprocess.Popen([resxtop,"--vihost",hostname,"-m"],env=my_env,stdout=mydata)
	thishostfh = open(hostname+".emcdata.scsidevs")
	thishostfh.write(p.stdout.read())
	thishostfh.close()

	
	
class myThread (threading.Thread):
	def __init__(self,hostname):
		self.hostname = hostname
		threading.Thread.__init__(self)
	def run(self):
		sys.stdout.write('Starting collection process for ' + self.hostname + '\n')
		output = run_esxtop(self.hostname)
	


def run_esxtop(hostname):
	my_env = os.environ
	my_env["VI_SESSIONFILE"] = "./.sessionfile"

	mydata = open(hostname+".emcdata.csv",'w')
	p = subprocess.Popen([resxtop,"--vihost",hostname,"-c",".esxtop50rc","-b","-d","60","-n",str(collectioninterval)],env=my_env,stdout=mydata)
	sys.stdout.write(hostname + '...started\n')



threadList = []
for hostname in hosts:
	thread = myThread(hostname)
	thread.start()

	threadList.append(thread)
	time.sleep(.2)


print "Collection Started.  Come back in " + str(comeback) + " hours and run submit.py"

	

	

	



