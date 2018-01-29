'''
this script merge all the data packets into one file

packets.sort(key=lambda pkt:pkt[0] + ' ' + pkt[1])

- sensor_data:
 result_time 	 node_id 	 parent_id 	 stats_frssi 	stats_brssi 	 letx 	 temperature 	 humidity 	voltage
 0, 1                2          3          4             5                 6           7        8              9

- summary and routing data:
 result_time 	 node_id 	 parent_id 	 stats_raw_frssi 	 stats_raw_brssi 	 etx 
 

**Format all data as the same as routing&summary

'''

import sys

SRC = 2
PARENT = 3
FRSSI = 4
BRSSI = 5
LETX = 6
TEMP = 7
HUM = 8
VOLT = 9

inf1 = open("processed_aswp_sensor_data20140807.txt", "r")
inf2 = open("processed_aswp_summary_data20140807.txt", "r")
inf3 = open("processed_aswp_routing_data20140807.txt", "r")

outf = open("all_data_20140807.txt", "w")

outf.writelines("result_time\tnode_id\tparent_id\tstats_frssi\tstats_brssi\tletx\ttemperature\thumidity\tvoltage\n")

packets = []
total_count = 0
## for sensor data
print "start to process sensor data"
lines = inf1.readlines()

line_count = 0
for line in lines:
	line_count += 1
	s = line.split()
	if line_count > 1:
		if len(s)>0:
			newpkt = s[0] + ' ' + s[1]
			for i in range(2, len(s)):
				newpkt += '\t' + s[i]
			newpkt += '\n'
			packets.append(newpkt)
			total_count += 1

print "sensor data line_count: " + str(line_count)
## for summary data
print "start to process summary data"
lines = inf2.readlines()

line_count = 0
for line in lines:
	line_count += 1
	s = line.split()
	if line_count > 1:
		if len(s)>0:
			newpkt = s[0] + ' ' + s[1]
			
			for i in range(2, len(s)):
				newpkt += '\t' + s[i]
			newpkt += '\n'
			packets.append(newpkt)
			total_count += 1

			
print "summary data line_count: " + str(line_count)

## for routing data
print "start to process routing data"
lines = inf3.readlines()

line_count = 0
for line in lines:
	line_count += 1
	s = line.split()
	if line_count > 1:
		if len(s)>0:
			newpkt = s[0] + ' ' + s[1]
			
			for i in range(2, len(s)):
				newpkt += '\t' + s[i]
			newpkt += '\n'
			packets.append(newpkt)
			total_count += 1


print "routing data line_count: " + str(line_count)

## sort the data by time
def getKey(pkt):
	return pkt[0] + ' ' + pkt[1]
	
print "total packet counts: " + str(total_count)
packets.sort()

for pkt in packets:
	outf.writelines(pkt)
	
inf1.close()
inf2.close()
inf3.close()
outf.close()