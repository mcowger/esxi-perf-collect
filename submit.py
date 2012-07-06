#!/usr/bin/python

from ftplib import FTP
import zipfile
import os
import string
import random
import glob
import hashlib
import subprocess
import sys

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open(file))
    else:
        ftp.storbinary("STOR " + file, open(file, "rb"), 1024)


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
myfile = zipfile.ZipFile(filebase+".zip",'w')
for filename in glob.glob('*.csv'):
	myfile.write(filename, os.path.basename(filename), zipfile.ZIP_DEFLATED)
	os.remove(filename)
myfile.close


print "Created zip file for upload: " + filebase + ".zip"
print "Attempting to upload to EMC Secure FTP..."
ftp = FTP('ftp.emc.com')
ftp.login()
ftp.cwd("/incoming")
upload(ftp,filebase + ".zip")
ftp.quit()
print "File (possibly) uploaded.  Inform your EMC representative to check CSFTP for the following file: ftp://csftp.emc.com/incoming/" + filebase + ".zip"
print "It should be ready in 20 minutes."
print "MD5 of the file is: " + md5_for_file(open(filebase + ".zip"))
print "...or you can simply email or FTP the above file manually."