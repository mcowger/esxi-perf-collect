#!/usr/bin/python


import zipfile
import os
import string
import random
import glob
import subprocess
import sys


def findprocessbyname(processname):
	return subprocess.Popen(["pidof",processname],stdout=subprocess.PIPE).stdout.read()

	
def processrunning(processname):
	if (len(findprocessbyname(processname)) > 0):
		return True
	return False	

print "Checking for still running processes..."
if (processrunning("resxtop")):
	print "Found resxtop running with PID:"
	print findprocessbyname("resxtop")
	keepgoing = raw_input("(a)bort? any other key to continue...")
	if (keepgoing == 'a' or keepgoing == 'A'): 
		print "Aborted"
		sys.exit(0)

randomstring = "".join(random.sample(string.letters+string.digits, 5))
filebase="emcdata." + randomstring
zipfilename = filebase + ".zip"
myfile = zipfile.ZipFile(zipfilename,'w')
for filename in glob.glob('*.csv'):
	myfile.write(filename, os.path.basename(filename), zipfile.ZIP_DEFLATED)
	os.remove(filename)
myfile.close()


print "Created zip file for upload: " + zipfilename
print "MD5 of the file is: " +  subprocess.Popen(["md5sum",zipfilename],stdout=subprocess.PIPE).stdout.read()
print "Attempting to upload to EMC Secure FTP..."
output = subprocess.Popen(["/usr/bin/curl","-T",zipfilename,"ftp://ftp.emc.com/incoming/"+zipfilename],stdout=subprocess.PIPE).stdout.read()
print output


print "File (possibly) uploaded.  Inform your EMC representative to check CSFTP for the following file: ftp://csftp.emc.com/incoming/" + zipfilename
print "It should be ready in 20 minutes."

print "...or you can simply email or FTP the above file manually."