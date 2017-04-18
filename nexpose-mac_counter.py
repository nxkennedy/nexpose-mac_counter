#! /usr/bin/env python3
###########################################################################
#
# [+] Description: Script that counts total of unique MAC addresses contained
# in a Nexpose asset discovery report
# [+] Use Case: Often Nexpose discovery scans of VIPs, VMs, and hypervisors
# return results of duplicate MAC addresses or no MAC at all. This tool sheds
# light on asset detection accuracy by determining unique MACs found, assets
# missing MACs, dupes, and the 10 most common dupes.
#
#                          ~ author: nxkennedy ~
###########################################################################

#******** Usage ********#
# python3 nexpose-mac_counter.py
#**********************#

# !!! IMPORTANT !!! THIS SCRIPT WAS BUILT TO PROCESS A CSV REPORT GENERATED
# WITH THE FOLLOWING NEXPOSE SQL QUERY:
"""

SELECT mac_address AS "MAC", da.ip_address AS "IP", host_name AS "Host Name",
dos.description AS "OS", dht.description AS "Host Type"
FROM fact_asset_discovery
  JOIN dim_asset da USING (asset_id)
  JOIN dim_operating_system dos USING (operating_system_id)
  JOIN dim_host_type dht USING (host_type_id)


"""

# Output of this script looks like:
"""

>> Stats for:  RandomSite-DiscoveryReport.csv
_____
> Active Assets Found in Scan:  1510
> Duplicate MACs:  124
> Hosts/IPs Without MACs:  1002
=====
> Total Unique MACs:  384
=====

> Top 10 Occuring Dupes:
84:80:69:fd:22:69 x 5
00:25:82:06:e0:70 x 4
4e:56:83:16:24:71 x 3
9a:81:19:84:76:72 x 3
8e:98:a5:24:26:73 x 3
00:25:86:06:74:cf x 3
7e:6a:85:9e:75:76 x 3
00:25:77:06:e1:ef x 3
46:87:d4:78:e3:60 x 3
82:88:91:79:6a:39 x 3

> Sample of Hosts Missing MACs:
['10.1.1.2', '']
['10.1.1.3', '']
['10.1.1.4', 'random-host1.com']
['10.1.1.5', 'random-host2.com]
['10.1.1.6', 'random-host3.com']
['10.1.1.7', '']
['10.1.1.8', 'random-host4.com']
['10.1.1.9', 'random-host5.com']
['10.1.1.10', '']
['10.1.1.11', 'random-host6.com']

"""



from collections import Counter # this is the bee's knees
import csv
import os
import sys



def output_formatter(csvReport, macPoor, macPoorCount, macRich, macRichCount, dupeList, dupeCount): # spits out final output to the terminal

    print("\n>> Stats for: ", csvReport)
    print("_____")
    print("> Active Assets Found in Scan: ", dupeCount + macRichCount + macPoorCount) # sums everything assessed in the file
    print("> Duplicate MACs: ", dupeCount)
    print("> Hosts/IPs Without MACs: ", macPoorCount)
    print("=====")
    print("> Total Unique MACs: ", macRichCount)
    print("=====\n")
    counter = Counter(dupeList)
    print("> Top 10 Occuring Dupes: ")
    for mac, occurence in counter.most_common(10):
        print("{0} x {1}".format(mac, occurence)) # Prints the 10 most commonly occuring MACs
    print("\n> Sample of Hosts Missing MACs:")
    for host in range(10):
        print(macPoor[host])
    print()



def csv_reader(csvReport): # Opens report for reading

    with open(csvReport) as csvfile:
        csvReader = csv.DictReader(csvfile)
        # Setup our lists and counters
        macPoor = []
        macPoorCount = 0
        macRich = []
        macRichCount = 0
        dupeList = []
        dupeCount = 0
        e = None  # This is our exception flag

        # Begin iteration of MAC column in report
        for row in csvReader:
            try:
                macAddr = row['MAC']

                if macAddr == '': # if no mac address
                    ipAndName = [row['IP'], row['Hostname']] # Required because append() takes only one arg
                    macPoor.append(ipAndName)
                    macPoorCount += 1
                elif macAddr in macRich: # or if the mac has already been seen
                    dupeList.append(macAddr)
                    dupeCount += 1
                else: # else write the mac to the list
                    macRich.append(macAddr)
                    macRichCount += 1

            except KeyError as exception:
                column = exception.args[0]
                print("\n****")
                print("> INPUT FILE '{0}' IS NOT FORMATTED CORRECTLY (READ THE SCRIPT)".format(csvReport))
                print("> MISSING DATA COLUMN: {0}".format(column))
                print("Continuing to next file. . .")
                print("****\n")
                e = exception
                break

            except Exception as exception:
                print("\n!!!!")
                print("> Unable to process file {0}".format(csvReport))
                print("> {0}".format(exception))
                print("Continuing to next file. . .")
                print("!!!!\n")
                e = exception
                break

    if not e:
        # Unless there's an exception, call function to format data
        output_formatter(csvReport, macPoor, macPoorCount, macRich, macRichCount, dupeList, dupeCount)

def csv_writer(csvReport):

    with open(, 'w+') as csvfile:
        csvWriter = csv.writer(csvfile)
        pass


def directory_search(dirListing):

    csvExists = None
    currentDir = os.getcwd()
    for fname in dirListing: # iterate over each filename in current directory

        if not fname.endswith('.csv'): # not csv? move on
            continue
        else:
            csvExists = True
            csv_reader(fname) # call function to start processing the csv

    if not csvExists:
        print("\n>> Hmm... No CSVs to process here in '{0}':\n".format(currentDir))
        for f in dirListing:
            print(f)
        print()


if __name__ == "__main__":
    dirListing = os.listdir('.')
    directory_search(dirListing)
