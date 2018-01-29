'''
This script find the dates at when most of the nodes are alive

Use node sensor data
'''

import sys
import time
SRC = 2
DAY = 0
TIME = 1


inf = open("processed_aswp_sensor_data20140807.txt", "r")

# store the number of nodes of each day
outf = open("node_number_per_day.txt", "w")		
outf_good_period = open("good_periods.txt", "w")

# store the nodes: key = nodeid, value = "Y" or "N"
all_nodes = {}

# the alive nodes each day 
# key = day, value: alive count
daily_alive = {}

lines = inf.readlines()

line_count = 0
cur_day = ""
pre_day = ""
alive_count = 0

for line in lines:
	line_count += 1
	if line_count == 1:
		continue
		
	s = line.split()
	if len(s) > 0:
		src = s[SRC]
		if line_count == 2:
			# the first packet
			pre_day = cur_day = s[DAY]
			
		cur_day = s[DAY]
		if pre_day != cur_day:
			# for each day, count the number of alive nodes
			# if the value is "Y" in all_nodes, then the node is alive
			
			alive_count = 0
			for id in all_nodes:
				if all_nodes[id] == "Y":
					alive_count += 1
			
			newline = pre_day + '\t' + str(alive_count) + '\n'
			outf.writelines(newline)
			
			daily_alive[pre_day] = alive_count
			
			pre_day = cur_day
			
			for id in all_nodes:
				all_nodes[id] = "N"
				
		else:
			# the same day
			if not all_nodes.has_key(src):
				# the node is not in the dict yet
				
				# the first day has 65 nodes???
				if cur_day == "2014-08-02":
					print src
				all_nodes[src] = "Y"
			
			all_nodes[src] = "Y"

inf.close()
outf.close()

start_date = ""
end_date = ""
days_count = 0

sorted_days = sorted(daily_alive)
for day in sorted_days:
	
	if daily_alive[day] >= 30:
		# if there are more than 30 nodes alive, consider it as good period
		if days_count == 0:
			start_date = day
		
		days_count += 1
	else:
		# the alive nodes is less than 30, period ends
		end_date = day 
		if days_count == 0:
			start_date = end_date
			continue
		newline = start_date + ' ' + end_date + '\t' + str(days_count) + '\n'
		outf_good_period.writelines(newline)
		
		start_date = end_date
		days_count = 0

newline = start_date + " " + sorted_days[len(sorted_days)-1] + '\t' + str(days_count) + '\n'
outf_good_period.writelines(newline)

outf_good_period.close()
		
			
			
		
		
		
