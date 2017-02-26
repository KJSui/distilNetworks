#!/usr/bin/python
import csv
from os import remove
from shutil import move
import matplotlib.pyplot as plt

class logEnrichment(object):
    def ipClass(self, number):
        """ decide the ip class based on ip address
        """
        if number >=0 and number < 128:
            return "A"
        if number >= 128 and number < 192:
            return "B"
        if number >= 192 and number < 224:
            return "C"
        if number >= 224 and number < 240:
            return "D"
        if number >= 240 and number < 256:
            return "E"

    def addIPClass(self, file):
        """Add a column before the ip address to the log file
            containing the IP Class of the accessing IP.
        """
        with open('new.tsv', 'w') as newFile:
            with open(file) as oldFile:
                tsvreader = csv.reader(oldFile, delimiter='\t')
                newFile = csv.writer(newFile, delimiter='\t')
                for line in tsvreader:
                    ip = line[2].split(".")
                    line.insert(2, self.ipClass(int(ip[0])))
                    newFile.writerow(line)
        remove(file)
        move('new.tsv', file)


    def IPRateLimiting(self, file):
        """Produce a file containing the average pages per minutes
            and average pages per session for each IP
        """
        with open('ipRateLimitingSummary.tsv', 'w') as newFile:
            start, pageCount, minuCount, average = -1, 0, 0, 0
            ipDic = {}
            with open(file) as oldFile:
                tsvreader = csv.reader(oldFile, delimiter='\t')
                newFile = csv.writer(newFile, delimiter='\t')
                for line in tsvreader:
                    timestamp = line[3]    ##get timestamp
                    pageCount += 1
                    if start == -1:        ## first line
                        start = timestamp
                    elif timestamp - start >= 60:  ##get page count per minute
                        minuCount += 1
                        average = pageCount/minuCount
                        start = timestamp

                    ip = line[2]
                    if ip not in ipDic:
                    ##initiate dict: key - ip, val - [pageCount and timestamp]
                        ipDic[ip] = [1, timestamp]
                    else:
                        if timestamp - ipDic[ip][1] <= 20*60 \
                        and timestamp -ipDic[ip][1] > 0:
                        ## if ip with session has not expired, add pagecount
                            ipDic[ip][0] += 1
                        else: ## add ip, session page count as a line into file
                            newFile.writerow([ip, ipDic[ip][0]])
                            ipDic[ip] = [1, timestamp]
                newFile.writerow([average])  ## add page average per minute

    def logAggregation(self, file):
        """ Produce a graph of aggregated status codes over time
        """
        statusList, timeList, start, sumStatusCode = [], [], -1, 0
        with open(file) as oldFile:
            tsvreader = csv.reader(oldFile, delimiter='\t')
            for line in tsvreader:
                timestamp = line[3]    ##get timestamp
                if start == -1:        ## first line
                    start = timestamp
                    sumStatusCode = line[5]
                elif timestamp - start > 2*60:  ##get page count per minute
                    statusList.append(asumStatusCode/2)
                    timeList.append(start)
                    start = timestamp
                    sumStatusCode = line[5]
                else:
                    sumStatusCode += line[5]
        plt.figure()
        plt.xlabel("timestamp per 2 minutes")
        plt.ylabel("status code average")
        plt.title("moving average 2 minutes status code")
        plt.plot(statusList, timeList)
        plt.savefig("logAggregation.png")
