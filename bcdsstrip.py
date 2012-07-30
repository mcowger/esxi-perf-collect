#!/usr/bin/python

import csv
import re

columnMatch = re.compile(r'Physical Disk\([\w+|\-|\:]+\)\\[Commands/sec|Reads/sec|Writes/sec|MBytes Read/sec|MBytes Written/sec]',re.S)

esxtopReader = csv.reader(open('corvir01.esxtop.20101014.txt','rb'),delimiter=',',quotechar='"')
filteredWriter = csv.writer(open('filtered.csv','wb'), delimiter=',')

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

