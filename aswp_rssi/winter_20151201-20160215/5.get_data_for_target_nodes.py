'''
get data packets for each target nodes
'''

import sys

SRC = 2
PARENT = 3

inf = open("winter_data2_20151201-20160215.txt", "r")
inf_targets = open("target_nodes.txt", "r")

# target nodes key = src, value = prnt
targets = {}
node_packets = {}

# load target nodes
lines = inf_targets.readlines()

for line in lines:
	print line
	s = line.split()
	if len(s) == 3:
		print line
		key = s[0] + "_" + s[1]
		targets[key] = 1
		node_packets[key] = []
		

print str(targets)

inf_targets.close()

# get data for each target nodes
lines = inf.readlines()

for line in lines:
	s = line.split()
	if len(s) > 0:
		src = s[SRC]
		prnt = s[PARENT]
		if src == "50431" or prnt == "50431": 
			continue
		key = src + "_" + prnt
		if targets.has_key(key):
				# if the packet matches
				node_packets[key].append(line)

for key in node_packets:
	outf = open("target_nodes_packets\\" + key + ".txt", "w")
	outf.writelines("result_time\tnode_id\tparent_id\tstats_frssi\tstats_brssi\tetx\ttemperature\thumidity\tvoltage\n")
	outf.writelines(node_packets[key])
	outf.close()
	
inf.close()

