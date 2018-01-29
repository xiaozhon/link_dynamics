'''
Get packets for 21631_11301, 
	get <frssi, temp> pairs, using sensor data
	sort based on temp,
	compute average rssi for each 0.5 C temp.

'''
import sys

SRC = 2
PARENT = 3
F_RSSI = 4		# in parent node
B_RSSI = 5		# in src node
ETX = 6
TEMP = 7
HUM = 8
VOLT = 9

DATA_LEN = 10

t_src = 21831
t_prnt = 10701

# store <temp, frssi> pairs
temp_frssi = []
avg_temp_frssi = []

inf = open("good_data4_2015-07-10-2015-09-20.txt", "r")
outf = open("data4_" + str(t_src) + "_" + str(t_prnt) + "_temp_rssi.txt", "w")

lines = inf.readlines()

for line in lines:
	s = line.split()
	if len(s) == DATA_LEN:
		if int(s[SRC]) == t_src and int(s[PARENT]) == t_prnt:
			temp_frssi.append([float(s[TEMP]), int(s[F_RSSI])])

# sort based on temp
temp_frssi.sort()

pre_temp = temp_frssi[0][0]

tmp_list = []

for i in range(0, len(temp_frssi)):
	# for each <temp, frssi> pairs, average them for every 0.5 C
	if temp_frssi[i][0] - pre_temp >= 0.5:
		# Reach 0.5 C, compute the average
		avg_rssi = 0.0
		avg_temp = 0.0
		for p in tmp_list:
			avg_temp += p[0]*1.0/len(tmp_list)
			avg_rssi += p[1]*1.0/len(tmp_list)
			
		avg_temp_frssi.append([avg_temp, avg_rssi])
		
		
		tmp_list = []
		pre_temp = temp_frssi[i][0]
	else:
		# the temperature is within 0.5 C, add the readings and continue
		tmp_list.append(temp_frssi[i])

outf.writelines("temp\tfrssi\n")
for p in avg_temp_frssi:
	outf.writelines(str(p[0]) + '\t' + str(p[1]) + '\n')

inf.close()
outf.close()
		