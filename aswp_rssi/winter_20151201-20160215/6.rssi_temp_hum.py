
SRC = 2
PARENT = 3
F_RSSI = 4		# in parent node
B_RSSI = 5		# in src node
ETX = 6
TEMP = 7
HUM = 8
VOLT = 9

DATA_LEN = 10

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import sys
import os


inf_targets = open("target_nodes.txt", "r")
inf_nodes = open("../nodes_info.txt", "r")
# key = nodeid, value = node type (Micaz, TelosB, IRIS)
nodes_info = {}

targets = []
# read in all the targets
t_lines = inf_targets.readlines()
for t_line in t_lines:
	t = t_line.split()
	if len(t) > 0:
		targets.append([t[0], t[1]])
		
inf_targets.close()

# read in nodes information
n_lines = inf_nodes.readlines()
for n_line in n_lines:
	n = n_line.split()
	if len(n) > 0:
		if n[1] == "0":
			nodes_info[n[0]] = "MicaZ"
		elif n[1] == "1":
			nodes_info[n[0]] = "IRIS"
		elif n[1] == "2":
			nodes_info[n[0]] = "TelosB"
		else:
			continue

inf_nodes.close()

'''
definition of ploting functoin
'''
	### compute average temp and frssi
def plot_temp_frssi(temp_rssi_list, link):
	temp_rssi_list.sort()
	pre_temp = temp_rssi_list[0][0]
	tmp_temp_list = []
	tmp_rssi_list = []
	
	p_temp = []
	p_rssi = []
	p_rssi_std = []		# the standard variance for each rssi_avg
	
	total_rssi_avg = 0
	for i in range(0, len(temp_rssi_list)):
		# for each <temp, frssi> pairs, average them for every 0.5 C
		if temp_rssi_list[i][0] - pre_temp >= 0.5:
			# Reach 0.5 C, compute the average
			avg_rssi = 0.0
			avg_temp = 0.0
			rssi_std = 0.0
		#	for p in tmp_list:
		#		avg_temp += p[0]*1.0/len(tmp_list)
		#		avg_rssi += p[1]*1.0/len(tmp_list)
	#		print "+++++ temp_rssi_list is: " + str(tmp_rssi_list)
			
			if len(tmp_rssi_list) <= 0:
				tmp_temp_list = []
				tmp_rssi_list = []
				pre_temp = temp_rssi_list[i][0]
				continue
			
			avg_rssi = np.mean(tmp_rssi_list)
			avg_temp = np.mean(tmp_temp_list)
			rssi_std = np.std(tmp_rssi_list)
			
			avg_temp_frssi.append([avg_temp, avg_rssi])
			
			if avg_temp != 0 and avg_rssi != 0 and avg_temp > -20:
				p_temp.append(avg_temp)
				p_rssi.append(avg_rssi)
				p_rssi_std.append(rssi_std)
				
				total_rssi_avg += avg_rssi
			
			tmp_temp_list = []
			tmp_rssi_list = []
			pre_temp = temp_rssi_list[i][0]
		else:
			# the temperature is within 0.5 C, add the readings and continue
	#		tmp_list.append(temp_frssi[i])
			tmp_temp_list.append(temp_rssi_list[i][0])
			tmp_rssi_list.append(temp_rssi_list[i][1])
	#print avg_temp_frssi
	
	#### plot figure
	total_rssi_avg = int(total_rssi_avg/len(p_rssi))
	
	# print p_temp
#	print link[0] + "->" + link[1]
	# plot and save the figure of each link, for unified rssi and temperature 
	# range
	rssi_err = p_rssi_std			# for error bar
	fig_t = plt.errorbar(p_temp, p_rssi, yerr=p_rssi_std, fmt='ro')
	
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Temperature / $^\circ$C")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_rssi main figure
	
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_rssi_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)	
	extra_max_label = "max_rssi: " + str("{0:.2f}".format(np.max(p_rssi))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
	extra_min_label = "min_rssi: " + str("{0:.2f}".format(np.min(p_rssi))) + " dBm"
	
	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
	extra_avg_label = "avg_rssi: " + str("{0:.2f}".format(np.mean(p_rssi))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label],
				loc='best')
	
	plt.axis([-20, 50, -97, -40])
	
	# draw a line on temperature 35
	plt.plot((35, 35), (-97, -45), 'b-')
	
	# "-56_10011_1_.png"
	plt.savefig("figures\\frssi_temp_unified\\" + nodes_info[link[0]] + "_" + str(total_rssi_avg) + "_" 
				+str(int(min(p_temp))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()
	
	# plot and save figures of each link, use max & min of the rssi and temp 
	# as the range
	fit_t = plt.errorbar(p_temp, p_rssi, yerr=p_rssi_std, fmt='ro')
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Temperature / $^\circ$C")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_rssi main figure	
	
	# add additional legend
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_rssi_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_max_label = "max_rssi: " + str("{0:.2f}".format(np.max(p_rssi))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_min_label = "min_rssi: " + str("{0:.2f}".format(np.min(p_rssi))) + " dBm"

	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_avg_label = "avg_rssi: " + str("{0:.2f}".format(np.mean(p_rssi))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label],
				loc='best')

	plt.axis([min(p_temp) - 1, 48, min(p_rssi) - max(p_rssi_std) - 0.5, max(p_rssi) + max(p_rssi_std) + 0.5])
	
	# draw a line on temperature 35
	plt.plot((35, 35), (min(p_rssi) - max(p_rssi_std) - 0.5, max(p_rssi) + max(p_rssi_std) + 0.5), 'b-')
	
	plt.savefig("figures\\frssi_temp\\"   + nodes_info[link[0]] + "_" + str(total_rssi_avg) + "_" 
				+str(int(min(p_temp))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()

	inf.close()
	
	########################################################################################
	########################################################################################
	
	### compute average hum and frssi
def plot_hum_frssi(hum_rssi_list, link):

	hum_rssi_list.sort()
	pre_hum = hum_rssi_list[0][0]
	tmp_rssi_list = []
	tmp_hum_list = []
	
	p_hum = []
	p_rssi = []
	p_rssi_std = []
	
	total_rssi_avg = 0
	for i in range(0, len(hum_rssi_list)):
		# for each <hum, frssi> pairs, average them for every 1%
		if hum_rssi_list[i][0] - pre_hum >= 0.5:
			# Reach 0.5%, compute the average
			avg_rssi = 0.0
			avg_hum = 0.0
			rssi_std = 0.0
			
	#		for p in tmp_list:
	#			avg_hum += p[0]*1.0/len(tmp_list)
	#			avg_rssi += p[1]*1.0/len(tmp_list)
				
			if len(tmp_rssi_list) <= 0:
				tmp_hum_list = []
				tmp_rssi_list = []
				pre_hum = hum_rssi_list[i][0]
				continue
			
			avg_rssi = np.mean(tmp_rssi_list)
			avg_hum = np.mean(tmp_hum_list)
			rssi_std = np.std(tmp_rssi_list)
			
			avg_hum_frssi.append([avg_hum, avg_rssi])
			
			if avg_hum > 0 and avg_rssi != 0 :
				p_hum.append(avg_hum)
				p_rssi.append(avg_rssi)
				p_rssi_std.append(rssi_std)
				
				total_rssi_avg += avg_rssi
	
			tmp_hum_list = []
			tmp_rssi_list = []
			pre_hum = hum_rssi_list[i][0]
		else:
			# the hum is within 0.5 C, add the readings and continue
			tmp_hum_list.append(hum_rssi_list[i][0])
			tmp_rssi_list.append(hum_rssi_list[i][1])
		
	# plot figure
	'''
	if len(tmp_rssi_list) > 0:
				
		avg_rssi = np.mean(tmp_rssi_list)
		avg_hum = np.mean(tmp_hum_list)
		rssi_std = np.std(tmp_rssi_list)
		
		avg_hum_frssi.append([avg_hum, avg_rssi])
		
		if avg_hum > 0 and avg_rssi != 0 :
			p_hum.append(avg_hum)
			p_rssi.append(avg_rssi)
			p_rssi_std.append(rssi_std)
			
			total_rssi_avg += avg_rssi
	'''		
		
	total_rssi_avg = int(total_rssi_avg/len(p_rssi))
	
		
	# plot and save the figure of each link, for unified rssi and temperature 
	# range
	fig_t = plt.errorbar(p_hum, p_rssi, yerr = p_rssi_std, fmt='bo')
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Humidity / %")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_rssi main figure	
	
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_rssi_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_max_label = "max_rssi: " + str("{0:.2f}".format(np.max(p_rssi))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_min_label = "min_rssi: " + str("{0:.2f}".format(np.min(p_rssi))) + " dBm"

	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_avg_label = "avg_rssi: " + str("{0:.2f}".format(np.mean(p_rssi))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
				, loc='best')

	plt.axis([20, 100, -95, -45])
	plt.xscale('linear')
	
	# draw a line on temperature 35
#	plt.plot((35, 35), (-95, -45), 'b-')
	
	# "-56_10011_1_.png"
	plt.savefig("figures\\frssi_hum_unified\\" + nodes_info[link[0]] + "_" + str(total_rssi_avg) + "_" 
				+str(int(min(p_hum))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()
	
	# plot and save figures of each link, use max & min of the rssi and temp 
	# as the range
		
	fig_t = plt.errorbar(p_hum, p_rssi, yerr = p_rssi_std, fmt='bo')
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Humidity / %")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_rssi main figure
	
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_rssi_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_max_label = "max_rssi: " + str("{0:.2f}".format(np.max(p_rssi))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_min_label = "min_rssi: " + str("{0:.2f}".format(np.min(p_rssi))) + " dBm"

	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_avg_label = "avg_rssi: " + str("{0:.2f}".format(np.mean(p_rssi))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
				, loc='best')
	plt.axis([min(p_hum) - 1, max(p_hum) + 1, min(p_rssi) - max(p_rssi_std) - 0.5, max(p_rssi) + max(p_rssi_std)+ 0.5])
	
	# draw a line on temperature 35
#	plt.plot((35, 35), (min(p_rssi) - 0.5, max(p_rssi) + 0.5), 'b-')
	
	plt.savefig("figures\\frssi_hum\\"   + nodes_info[link[0]] + "_" + str(total_rssi_avg) + "_" 
				+str(int(min(p_hum))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()


### p[i] = [temp, hum, rssi]
### for each temp: 		# -5, 0, 5, 10, 15, 20, ...
###		sort [hum, rssi] pair
###		Average rssi on hum 
### 	plot figure for the average
###
def plot_temp_hum_frssi(temp_hum_rssi_list, link):
	temp_hum_rssi_list.sort()
	temps = []
	for entry in temp_hum_rssi_list:
		# get all the temperature readings
		temps.append(entry[0])	
		
	min_temp = min(temps)
	
	
	pre_temp = min_temp
	
	if min_temp >= 0:
		temp_idx = int(min_temp / 5)	# split each temperature by every 5 C
		temp_rest = min_temp - temp_idx*5
		if temp_rest >= 2.5:	# for each temperature T, average hum and rssi
								# within [T-2.5, T+2.5]
			temp_idx += 1
	else:
		# min_temp < 0
		temp_idx = int(min_temp/5)
		temp_rest = temp_idx*5 - min_temp
		if temp_rest >= 2.5:
			temp_idx -= 1
	
#	print "min_temp is: " + str(min_temp) + ", temp_idx is: " + str(temp_idx)
	###
#	tmp_temp_list = []
#	tmp_rssi_list = []
#	
#	p_temp = []
#	p_rssi = []
#	p_rssi_std = []		# the standard variance for each rssi_avg
	
#	total_rssi_avg = 0

	# key = temperature, value = [hum, rssi]
	T_hum_frssi = {}	
	
	for i in range(0, len(temp_hum_rssi_list)):
		# for each <temp, hum, frssi> pairs, get <hum, frssi> pair for every temperature
#		print "current temp is: " + str(temp_hum_rssi_list[i][0])
#		print "-	temp diff is: " + str(temp_hum_rssi_list[i][0] - temp_idx*5)
		
		if abs(temp_hum_rssi_list[i][0] - temp_idx*5) > 2.5:
			# the end of the previous temperature range
			# the start of next temperature range
			# update temperature index
			temp_idx += 1
#			print "+++++++++++cur temp_idx is: " + str(temp_idx)
			
		else:
			# store hum and frssi pairs for this temperature
			if not T_hum_frssi.has_key(str(temp_idx*5)):
				T_hum_frssi[str(temp_idx*5)] = []
			T_hum_frssi[str(temp_idx*5)].append([temp_hum_rssi_list[i][1], temp_hum_rssi_list[i][2]])
	
	
	for T in T_hum_frssi:
		# for each temperature, draw figures about <hum, frssi>
		hum_frssi_list = T_hum_frssi[T]		# get the <hum, frssi> pairs
		
		## actuall this should call plot_hum_frssi(hum_frssi_list, link)
		## however, the path is different, the figures are also slightly different
		
		hum_frssi_list.sort()
		pre_hum = hum_frssi_list[0][0]
		tmp_rssi_list = []
		tmp_hum_list = []
	
		p_hum = []
		p_rssi = []
		p_rssi_std = []
	
		total_rssi_avg = 0
		
#		if link[0] == "10501" and link[1] == "10301":
#			print "\ttemp is: " + T 
#			print "\t" + str(hum_frssi_list)
			
		for i in range(0, len(hum_frssi_list)):
			
			# for each <hum, frssi> pairs, average them for every 1%
			if hum_frssi_list[i][0] - pre_hum >= 0.25:
				# Reach 0.5%, compute the average
				avg_rssi = 0.0
				avg_hum = 0.0
				rssi_std = 0.0
				
				if len(tmp_rssi_list) <= 0:
					tmp_hum_list = []
					tmp_rssi_list = []
					pre_hum = hum_frssi_list[i][0]
					continue
				
				avg_rssi = np.mean(tmp_rssi_list)
				avg_hum = np.mean(tmp_hum_list)
				rssi_std = np.std(tmp_rssi_list)
				
				avg_hum_frssi.append([avg_hum, avg_rssi])
				
				if avg_hum > 0 and avg_rssi != 0 :
					p_hum.append(avg_hum)
					p_rssi.append(avg_rssi)
					p_rssi_std.append(rssi_std)
					
					total_rssi_avg += avg_rssi
					
#					if link[0] == "10501" and link[1] == "10301":
#						print "\p_rssi is: " + str(p_rssi)
		
				tmp_hum_list = []
				tmp_rssi_list = []
				pre_hum = hum_frssi_list[i][0]
			else:
				tmp_hum_list.append(hum_frssi_list[i][0])
				tmp_rssi_list.append(hum_frssi_list[i][1])
			
		
		## process the last few readings
		
		if len(tmp_rssi_list) > 0:
				
			avg_rssi = np.mean(tmp_rssi_list)
			avg_hum = np.mean(tmp_hum_list)
			rssi_std = np.std(tmp_rssi_list)
			
			avg_hum_frssi.append([avg_hum, avg_rssi])
			
			if avg_hum > 0 and avg_rssi != 0 :
				p_hum.append(avg_hum)
				p_rssi.append(avg_rssi)
				p_rssi_std.append(rssi_std)
				
				total_rssi_avg += avg_rssi
		
		if len(p_rssi) <= 0:
			continue
		
		
		total_rssi_avg = int(total_rssi_avg/len(p_rssi))
		
		# plot figure
		# plot and save the figure of each link, for unified rssi and temperature 
		# range
		fig_t = plt.errorbar(p_hum, p_rssi, yerr = p_rssi_std, fmt='bo')
		plt.ylabel("RSSI / dBm")
		plt.xlabel("Humidity / %")
		
		fig_title = link[0]+ r'$\rightarrow$' + link[1] + ", " + T + " $^\circ$C"
		plt.title(fig_title, loc='center')	# lable for temp_rssi main figure	
		
		extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_rssi_std))) + " dBm"
		
		extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_max_label = "max_rssi: " + str("{0:.2f}".format(np.max(p_rssi))) + " dBm"
		
		extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_min_label = "min_rssi: " + str("{0:.2f}".format(np.min(p_rssi))) + " dBm"

		extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_avg_label = "avg_rssi: " + str("{0:.2f}".format(np.mean(p_rssi))) + " dBm"

		plt.legend([extra_max, extra_min, extra_avg, extra_std], 
					[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
					, loc='best')

		plt.axis([20, 100, -95, -45])
		plt.xscale('linear')
		
		fig_dir = "figures\\temp_hum_frssi_unified\\" + str(int(T) + 100) + "-100_C"
		if not os.path.exists(fig_dir):
			os.makedirs(fig_dir)
		
		# "-56_10011_1_.png"
		plt.savefig(fig_dir + "\\"+ nodes_info[link[0]] + "_" + str(int(T) + 100) + "_" 
						+ str(int(min(p_hum))) + "_"  + str(total_rssi_avg) + "_" 
						+ link[0] + "_" + link[1] + ".png")
		plt.clf()
		
		# plot and save figures of each link, use max & min of the rssi and temp 
		# as the range
			
		fig_t = plt.errorbar(p_hum, p_rssi, yerr = p_rssi_std, fmt='bo')
		plt.ylabel("RSSI / dBm")
		plt.xlabel("Humidity / %")
		
		plt.title(fig_title, loc='center')	# lable for temp_rssi main figure
		
		extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_rssi_std))) + " dBm"
		
		extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_max_label = "max_rssi: " + str("{0:.2f}".format(np.max(p_rssi))) + " dBm"
		
		extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_min_label = "min_rssi: " + str("{0:.2f}".format(np.min(p_rssi))) + " dBm"

		extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_avg_label = "avg_rssi: " + str("{0:.2f}".format(np.mean(p_rssi))) + " dBm"

		plt.legend([extra_max, extra_min, extra_avg, extra_std], 
					[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
					, loc='best')
		plt.axis([min(p_hum) - 1, max(p_hum) + 1, min(p_rssi) - max(p_rssi_std) - 0.5, max(p_rssi) + max(p_rssi_std)+ 0.5])
		
		# draw a line on temperature 35
	#	plt.plot((35, 35), (min(p_rssi) - 0.5, max(p_rssi) + 0.5), 'b-')
		
		fig_dir = "figures\\temp_hum_frssi\\" + str(int(T) + 100) + "-100_C"
		if not os.path.exists(fig_dir):
			os.makedirs(fig_dir)
			
		plt.savefig(fig_dir + "\\"+ nodes_info[link[0]] + "_" + str(int(T) + 100) + "_" 
						+ str(int(min(p_hum))) + "_"  + str(total_rssi_avg) + "_" 
						+ link[0] + "_" + link[1] + ".png")
		plt.clf()
	
	########################################################################################
	########################################################################################

### end of function definition

###################################################################################
# Main processing loop
###################################################################################
# for each target, draw the figure
for t in targets:
	
	# 10011_1
#	if t[0] != "10011" or t[1] != "1":
#		continue
	
	
	if not os.path.exists("figures"):
		os.makedirs("figures")
		
	if not os.path.exists("figures\\frssi_hum"):
		os.makedirs("figures\\frssi_hum")
	if not os.path.exists("figures\\frssi_hum_unified"):
		os.makedirs("figures\\frssi_hum_unified")	
		
	if not os.path.exists("figures\\frssi_temp"):
		os.makedirs("figures\\frssi_temp")
	if not os.path.exists("figures\\frssi_temp_unified"):
		os.makedirs("figures\\frssi_temp_unified")
	
	if not os.path.exists("figures\\temp_hum_frssi"):
		os.makedirs("figures\\temp_hum_frssi")
	if not os.path.exists("figures\\temp_hum_frssi_unified"):
		os.makedirs("figures\\temp_hum_frssi_unified")
	
	
	inf = open("target_nodes_packets\\" + t[0] + "_" + t[1] + ".txt", "r")

	lines = inf.readlines()

	temp_frssi = []
	avg_temp_frssi = []
	
	hum_frssi = []
	avg_hum_frssi = []

	temp_hum_frssi = []
	
	line_count = 0

	for line in lines:
		line_count += 1
		if line_count > 1:
			s = line.split()
			if len(s) == DATA_LEN :
				if float(s[F_RSSI]) == -97:
					continue
				temp_frssi.append([float(s[TEMP]), float(s[F_RSSI])])
				hum_frssi.append([float(s[HUM]), float(s[F_RSSI])])
				temp_hum_frssi.append([float(s[TEMP]), float(s[HUM]), float(s[F_RSSI])])
	
	plot_temp_frssi(temp_frssi, t)
	plot_hum_frssi(hum_frssi, t)
	
	print t[0] + " -> " + t[1]
	
#	if t[0] == "10011" and t[1] == "1":
		# plot figure for link 10011_1
	plot_temp_hum_frssi(temp_hum_frssi, t)
	
	inf.close()
