#!/usr/bin/python

import csv
import re
import optparse
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--infile", dest="outfilename",
                  help="read stripped data from FILE", metavar="FILE")
parser.add_option("-o", "--outfile", dest="infilename",
                  help="write stripped data to FILE", metavar="FILE")

(options, args) = parser.parse_args()

columnMatch = re.compile(r'Physical Disk\([\w+|\-|\:]+\)\\[Commands/sec|Reads/sec|Writes/sec|MBytes Read/sec|MBytes Written/sec]',re.S)

print options.outfilename
print options.infilename



esxtopReader = csv.reader(open(options.outfilename,'rb'),delimiter=',',quotechar='"')
filteredWriter = csv.writer(open(options.infilename,'wb'), delimiter=',')




curIndex = 0
colIndexesIWant = [0]

headerLine = esxtopReader.next()
newHeaderLine = []
newHeaderLine.append('(PDH-CSV 4.0) (EST)(0)')
for columnName in headerLine:
	print "Considering " + columnName
	#print columnName
	if columnMatch.search(columnName):
		print "Keeping index " + columnName + " @ " + str(curIndex)
		colIndexesIWant.append(curIndex)
		newHeaderLine.append(columnName.strip())
	
	curIndex = curIndex + 1
print "Desired indexes " + str(colIndexesIWant)

filteredWriter.writerow(newHeaderLine)

totalLines = 0
for dataLine in esxtopReader:
	totalLines = totalLines + 1
	filteredDataLine = []
	for neededIndex in colIndexesIWant:
		#print "Copying index " + str(neededIndex) + " to filtered for line"
		filteredDataLine.append(dataLine[neededIndex].strip())

	filteredWriter.writerow(filteredDataLine)

print "Processed " + str(totalLines) + " total lines"

