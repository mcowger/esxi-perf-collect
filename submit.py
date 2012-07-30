#!/usr/bin/python

import csv
import re
import zipfile
import os
import string
import random
import glob
import subprocess
import sys
from optparse import OptionParser


def doBCSDfilter(filename):
	columnMatch = re.compile(r'Physical Disk\([\w+|\-|\:]+\)\\[Commands/sec|Reads/sec|Writes/sec|MBytes Read/sec|MBytes Written/sec]',re.S)
	esxtopReader = csv.reader(open(filename,'rb'),delimiter=',',quotechar='"')
	filteredWriter = csv.writer(open(filename + '.bcsd.filtered.csv','wb'), delimiter=',')
	curIndex = 0
	colIndexesIWant = [0]
	headerLine = esxtopReader.next()
	newHeaderLine = []
	newHeaderLine.append('(PDH-CSV 4.0) (EST)(0)')
	for columnName in headerLine:
		#print "Considering " + columnName
		#print columnName
		if columnMatch.search(columnName):
			#print "Keeping index " + columnName + " @ " + str(curIndex)
			colIndexesIWant.append(curIndex)
			newHeaderLine.append(columnName.strip())
		
		curIndex = curIndex + 1
	#print "Desired indexes " + str(colIndexesIWant)

	filteredWriter.writerow(newHeaderLine)

	totalLines = 0
	for dataLine in esxtopReader:
		totalLines = totalLines + 1
		filteredDataLine = []
		for neededIndex in colIndexesIWant:
			#print "Copying index " + str(neededIndex) + " to filtered for line"
			filteredDataLine.append(dataLine[neededIndex].strip())

		filteredWriter.writerow(filteredDataLine)
	print "Processed " + str(totalLines) + " total lines for BCSD output for " + filename


def findprocessbyname(processname):
	return subprocess.Popen(["ps -ef | grep resxtop | grep -v grep"],shell=True,stdout=subprocess.PIPE).stdout.read()

	
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
f = open("emc_esxscan.emcdata.txt","w")
f.close()
for filename in glob.glob('*.emcdata.csv'):
	doBCSDfilter(filename)
for filename in glob.glob('*.emcdata.*'):
	myfile.write(filename, os.path.basename(filename), zipfile.ZIP_DEFLATED)
myfile.close()


print "Created zip file for upload: " + zipfilename
print "MD5 of the file is: " +  subprocess.Popen(["md5sum",zipfilename],stdout=subprocess.PIPE).stdout.read()
print "Attempting to upload to EMC Secure FTP..."
output = subprocess.Popen(["/usr/bin/curl","-T",zipfilename,"ftp://ftp.emc.com/incoming/"+zipfilename],stdout=subprocess.PIPE).stdout.read()
print output


print "File (possibly) uploaded.  Inform your EMC or partner representative to check CSFTP for the following file: ftp://csftp.emc.com/incoming/" + zipfilename
print "It should be ready in 5 minutes."

print "...or you can simply email or FTP the above file manually."