'''
count the number of packets for each node, in order to select 
the target nodes for analysis

2014-08-02 09:17:55.456	10801	1	-88	-82	10	2.399	76.24	26.31


'''
import sys

SRC = 2
PARENT = 3

inf = open("good_data4_2015-07-10-2015-09-20.txt", "r")

inf_nodes = open("../nodeids.txt", "r")

outf_st = open("nodes_packet_count.txt", "w")
outf_st.writelines("id\tpacket_count\n")

# store <nodeid, packet_count> pair
nodes = {}
'''
lines = inf_nodes.readlines()

for line in lines:
	s = line.split()
	if len(s) > 0:
		nodes[s[0]] = 0
	
inf_nodes.close()
'''

# read packets
lines = inf.readlines()

for line in lines:
	s = line.split()
	if len(s) > 0:
		if s[SRC] == "50431" or s[PARENT] == "50431":
			continue
		key = s[SRC] + '\t' + s[PARENT]
		if not nodes.has_key(key):
			nodes[key] = 1
		else:
			nodes[key] += 1

inf.close()

# this one only sort the key, and only returns the key, not the 
# <key, value> pair
#sorted_nodes = sorted(nodes)	

# sort the "nodes" by their value.
sorted_nodes = sorted(nodes, key=nodes.get, reverse=True)	
for key in sorted_nodes:
	outf_st.writelines(key + '\t' + str(nodes[key]) + '\n')

outf_st.close()


