'''
1. correct the rssi value
2. fill the summary and routing packets with the temperature and humidity,
   use the average between two packets.

The rssi values in the data base is incorrect. Convert them to the correct one.

"frssi" come from the src node, "brssi" come from the parent node. Thus 
	result_time	 node_id	parent_id	stats_frssi	 stats_brssi	etx	temperature 	humidity voltage

	2014-08-02 09:17:55.456	10801	1	-88	-82	10	2399	7624	2631
	
	2014-09-01 09:23:24.407	20711	10501	2	2	10


The gateway converts all the rssi value using the formula of CC2420:
	*********************************************************************
	static public int get_rssi(RctpDataPacket_v4 packet, Short rssi){
		
		/*
		For MICAZ and Telosb (CC2420), the formula is:
		       real_val = read_rssi - 45

		For IRIS mote (RF230), the formula is:
		      real_val = 3*(read_rssi - 1) - 91
		
		*/
		
		int real_rssi = rssi;
		if(rssi >= 128){
			real_rssi = rssi - 256;
		}
		
		if(packet.get_motetype() == 1){  // IRIS mote
			return 3*(real_rssi - 1) - 91;
		}
		
		return (real_rssi - 45);
	}		
	************************************************************************

Summary and routing packets: 
	raw rssi

Sensor packets:
	converted using the above formula
	
	
micaz & telosb:
	raw = converted + 45

IRIS:
	raw = (converted + 91) / 3 + 1
'''
import sys
MICAZ = 0
IRIS = 1
TELOSB = 2

SRC = 2
PARENT = 3
F_RSSI = 4		# in parent node
B_RSSI = 5		# in src node
ETX = 6
TEMP = 7
HUM = 8
VOLT = 9

## functions
def converted_to_raw(motetype, value):
	if motetype == MICAZ or motetype == TELOSB:
#		print "-		back is: " + str(value + 45) + ", motetype is: " + str(motetype)
		return value + 45
	else: # motetype == IRIS:
		return (value + 91)/3 + 1

# convert raw rssi readings
def raw_to_converted(motetype, raw):
	if raw >= 128:
		raw = raw - 256
#	print "-		raw is: " + str(raw) + ", motetype is: " + str(motetype)
	if motetype == MICAZ or motetype == TELOSB:
#		print "-		rssi is: " + str(raw - 45)
		return raw - 45
	else: # motetype == IRIS:
#		print "-		rssi is: " + str(3*(raw - 1) - 91)
		return 3*(raw - 1) - 91

## main process

inf = open("all_data_20140807.txt", "r")
inf_nodes = open("nodes_info.txt", "r")

outf = open("all_data_20140807_rssi_corrected.txt", "w")
outf_err = open("all_error_packets.txt", "w")

'''
inf = open("test_packets_rssi.txt", "r")
inf_nodes = open("nodes_info.txt", "r")
outf = open("test_packets_rssi_corrected.txt", "w")
outf_err = open("test_error_packets.txt", "w")
'''

# store the node information
nodes = {}

# get the nodes information
lines = inf_nodes.readlines()
line_count = 0
for line in lines:
	line_count += 1
	if line_count > 1:
		s = line.split()
		if len(s) > 0:
			nodes[s[0]] = int(s[1])

inf_nodes.close()

#######################################################################
# TODO: fill the summary and routing with sensor data
# store the most recent node readings
node_readings = {}

# store the summary and routing packets.
# for a packet from "src", use the sensor_data to fill the temp and hum
temp_packets = []	
########################################################################
# TODO: or leave the data as it is.

# convert the data packets
lines = inf.readlines()
line_count = 0
newline = ""
for line in lines:
	line_count += 1
	
	if line_count > 1:
		s = line.split()
		if not nodes.has_key(s[SRC]) or not nodes.has_key(s[PARENT]):
			# packets with unknown node id
			continue
		
#		print line 
		
		if len(s) == 10:
			# sensor data
			raw_frssi = converted_to_raw(nodes[s[SRC]], int(s[F_RSSI]))
			raw_brssi = converted_to_raw(nodes[s[SRC]], int(s[B_RSSI]))
	#		print "-	parent is: " + s[PARENT]
			frssi = raw_to_converted(nodes[s[PARENT]], raw_frssi)
	#		print "-	SRC is: " + s[SRC] + ", type is: " + str(nodes[s[SRC]])
			brssi = raw_to_converted(nodes[s[SRC]], raw_brssi)
		if len(s) == 7:
			# summary and routing data
	#		print "-	parent is: " + s[PARENT]
			frssi = raw_to_converted(nodes[s[PARENT]], int(s[F_RSSI]))
	#		print "-	SRC is: " + s[SRC]
			brssi = raw_to_converted(nodes[s[SRC]], int(s[B_RSSI]))
			
		newline = s[0] + ' ' + s[1] + '\t' + s[SRC] + '\t' + s[PARENT]
		
		newline += '\t' + str(frssi) + '\t' + str(brssi) + '\t' + s[ETX]
		
		if len(s) == 10:
			newline += '\t' + str(int(s[TEMP])*1.0/100)
			newline += '\t' + str(int(s[HUM])*1.0/100)
			newline += '\t' + str(int(s[VOLT])*1.0/1000)
			
		newline += '\n'
		if len(s) == 10:
			if int(s[VOLT])*1.0/1000 < 2.2 or int(s[HUM]) < 0 or int(s[HUM])*1.0/100 > 100:
				# voltage is too low, the temperature readings are incorrect
				outf_err.writelines(newline)
			else:
				outf.writelines(newline)
		else:
			outf.writelines(newline)
	else:
		outf.writelines(line)
	
inf.close()
outf.close()





