
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
	### compute average temp and etx
def plot_temp_etx(temp_etx_list, link, dir):
	temp_etx_list.sort()
	pre_temp = temp_etx_list[0][0]
	tmp_temp_list = []
	tmp_etx_list = []
	
	p_temp = []
	p_etx = []
	p_etx_std = []		# the standard variance for each etx_avg
	
	total_etx_avg = 0
	for i in range(0, len(temp_etx_list)):
		# for each <temp, etx> pairs, average them for every 0.5 C
		if temp_etx_list[i][0] - pre_temp >= 0.5:
			# Reach 0.5 C, compute the average
			avg_etx = 0.0
			avg_temp = 0.0
			etx_std = 0.0
		#	for p in tmp_list:
		#		avg_temp += p[0]*1.0/len(tmp_list)
		#		avg_etx += p[1]*1.0/len(tmp_list)
	#		print "+++++ temp_etx_list is: " + str(tmp_etx_list)
			
			if len(tmp_etx_list) <= 0:
				tmp_temp_list = []
				tmp_etx_list = []
				pre_temp = temp_etx_list[i][0]
				continue
			
			avg_etx = np.mean(tmp_etx_list)
			avg_temp = np.mean(tmp_temp_list)
			etx_std = np.std(tmp_etx_list)
			
			avg_temp_etx.append([avg_temp, avg_etx])
			
			if avg_temp != 0 and avg_etx != 0 and avg_temp > -20:
				p_temp.append(avg_temp)
				p_etx.append(avg_etx)
				p_etx_std.append(etx_std)
				
				total_etx_avg += avg_etx
			
			tmp_temp_list = []
			tmp_etx_list = []
			pre_temp = temp_etx_list[i][0]
		else:
			# the temperature is within 0.5 C, add the readings and continue
	#		tmp_list.append(temp_etx[i])
			tmp_temp_list.append(temp_etx_list[i][0])
			tmp_etx_list.append(temp_etx_list[i][1])
	#print avg_temp_etx
	
	#### plot figure
	if len(p_etx) <= 0:
		print "------------no temp_etx figure for: " + str(link)
		print "\t\treadings are: " + str(temp_etx_list)	
		return
		
	total_etx_avg = int(total_etx_avg/len(p_etx))
	
	# print p_temp
#	print link[0] + "->" + link[1]
	# plot and save the figure of each link, for unified etx and temperature 
	# range
	etx_err = p_etx_std			# for error bar
	fig_t = plt.errorbar(p_temp, p_etx, yerr=p_etx_std, fmt='ro')
	
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Temperature / $^\circ$C")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_etx main figure
	
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_etx_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)	
	extra_max_label = "max_etx: " + str("{0:.2f}".format(np.max(p_etx))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
	extra_min_label = "min_etx: " + str("{0:.2f}".format(np.min(p_etx))) + " dBm"
	
	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
	extra_avg_label = "avg_etx: " + str("{0:.2f}".format(np.mean(p_etx))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label],
				loc='best')
	
	plt.axis([-20, 50, 0, 255])
	
	# draw a line on temperature 35
	plt.plot((35, 35), (0, 255), 'b-')
	
	# "-56_10011_1_.png"
	plt.savefig(dir + "_unified\\" + nodes_info[link[0]] + "_" + str(total_etx_avg) + "_" 
				+str(int(min(p_temp))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()
	
	# plot and save figures of each link, use max & min of the etx and temp 
	# as the range
	fit_t = plt.errorbar(p_temp, p_etx, yerr=p_etx_std, fmt='ro')
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Temperature / $^\circ$C")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_etx main figure	
	
	# add additional legend
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_etx_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_max_label = "max_etx: " + str("{0:.2f}".format(np.max(p_etx))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_min_label = "min_etx: " + str("{0:.2f}".format(np.min(p_etx))) + " dBm"

	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_avg_label = "avg_etx: " + str("{0:.2f}".format(np.mean(p_etx))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label],
				loc='best')

	plt.axis([min(p_temp) - 1, 48, min(p_etx) - max(p_etx_std) - 5, max(p_etx) + max(p_etx_std) + 5])
	
	# draw a line on temperature 35
	plt.plot((35, 35), (min(p_etx) - max(p_etx_std) - 5, max(p_etx) + max(p_etx_std) + 5), 'b-')
	
	plt.savefig(dir + "\\"   + nodes_info[link[0]] + "_" + str(total_etx_avg) + "_" 
				+str(int(min(p_temp))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()

	inf.close()
	
	########################################################################################
	########################################################################################
	
	### compute average hum and etx
def plot_hum_etx(hum_etx_list, link, dir):

	hum_etx_list.sort()
	pre_hum = hum_etx_list[0][0]
	tmp_etx_list = []
	tmp_hum_list = []
	
	p_hum = []
	p_etx = []
	p_etx_std = []
	
	total_etx_avg = 0
	for i in range(0, len(hum_etx_list)):
		# for each <hum, etx> pairs, average them for every 1%
		if hum_etx_list[i][0] - pre_hum >= 0.5:
			# Reach 0.5%, compute the average
			avg_etx = 0.0
			avg_hum = 0.0
			etx_std = 0.0
			
	#		for p in tmp_list:
	#			avg_hum += p[0]*1.0/len(tmp_list)
	#			avg_etx += p[1]*1.0/len(tmp_list)
				
			if len(tmp_etx_list) <= 0:
				tmp_hum_list = []
				tmp_etx_list = []
				pre_hum = hum_etx_list[i][0]
				continue
			
			avg_etx = np.mean(tmp_etx_list)
			avg_hum = np.mean(tmp_hum_list)
			etx_std = np.std(tmp_etx_list)
			
			avg_hum_etx.append([avg_hum, avg_etx])
			
			if avg_hum > 0 and avg_etx != 0 :
				p_hum.append(avg_hum)
				p_etx.append(avg_etx)
				p_etx_std.append(etx_std)
				
				total_etx_avg += avg_etx
	
			tmp_hum_list = []
			tmp_etx_list = []
			pre_hum = hum_etx_list[i][0]
		else:
			# the hum is within 0.5 C, add the readings and continue
			tmp_hum_list.append(hum_etx_list[i][0])
			tmp_etx_list.append(hum_etx_list[i][1])
		
	# plot figure
	'''
	if len(tmp_etx_list) > 0:
				
		avg_etx = np.mean(tmp_etx_list)
		avg_hum = np.mean(tmp_hum_list)
		etx_std = np.std(tmp_etx_list)
		
		avg_hum_etx.append([avg_hum, avg_etx])
		
		if avg_hum > 0 and avg_etx != 0 :
			p_hum.append(avg_hum)
			p_etx.append(avg_etx)
			p_etx_std.append(etx_std)
			
			total_etx_avg += avg_etx
	'''		
	#### plot figure
	if len(p_etx) <= 0:
		print "------------no hum_etx figure for: " + str(link)
		print "\t\treadings are: " + str(hum_etx_list)	
		return
	
	total_etx_avg = int(total_etx_avg/len(p_etx))
	
		
	# plot and save the figure of each link, for unified etx and temperature 
	# range
	fig_t = plt.errorbar(p_hum, p_etx, yerr = p_etx_std, fmt='bo')
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Humidity / %")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_etx main figure	
	
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_etx_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_max_label = "max_etx: " + str("{0:.2f}".format(np.max(p_etx))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_min_label = "min_etx: " + str("{0:.2f}".format(np.min(p_etx))) + " dBm"

	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_avg_label = "avg_etx: " + str("{0:.2f}".format(np.mean(p_etx))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
				, loc='best')

	plt.axis([20, 100, 0, 255])
	plt.xscale('linear')
	
	# draw a line on temperature 35
#	plt.plot((35, 35), (-95, -45), 'b-')
	
	# "-56_10011_1_.png"
	plt.savefig(dir + "_unified\\" + nodes_info[link[0]] + "_" + str(total_etx_avg) + "_" 
				+str(int(min(p_hum))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()
	
	# plot and save figures of each link, use max & min of the etx and temp 
	# as the range
		
	fig_t = plt.errorbar(p_hum, p_etx, yerr = p_etx_std, fmt='bo')
	plt.ylabel("RSSI / dBm")
	plt.xlabel("Humidity / %")
	
	plt.title(link[0]+ r'$\rightarrow$' + link[1], loc='center')	# lable for temp_etx main figure
	
	extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_etx_std))) + " dBm"
	
	extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_max_label = "max_etx: " + str("{0:.2f}".format(np.max(p_etx))) + " dBm"
	
	extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_min_label = "min_etx: " + str("{0:.2f}".format(np.min(p_etx))) + " dBm"

	extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
			linewidth=0)
			
	extra_avg_label = "avg_etx: " + str("{0:.2f}".format(np.mean(p_etx))) + " dBm"

	plt.legend([extra_max, extra_min, extra_avg, extra_std], 
				[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
				, loc='best')
	plt.axis([min(p_hum) - 1, max(p_hum) + 1, min(p_etx) - max(p_etx_std) - 0.5, max(p_etx) + max(p_etx_std)+ 0.5])
	
	# draw a line on temperature 35
#	plt.plot((35, 35), (min(p_etx) - 0.5, max(p_etx) + 0.5), 'b-')
	
	plt.savefig(dir + "\\"   + nodes_info[link[0]] + "_" + str(total_etx_avg) + "_" 
				+str(int(min(p_hum))) + "_" + link[0] + "_" + link[1] + ".png")
	plt.clf()


### p[i] = [temp, hum, etx]
### for each temp: 		# -5, 0, 5, 10, 15, 20, ...
###		sort [hum, etx] pair
###		Average etx on hum 
### 	plot figure for the average
###
def plot_temp_hum_etx(temp_hum_etx_list, link, dir):
	temp_hum_etx_list.sort()
	temps = []
	for entry in temp_hum_etx_list:
		# get all the temperature readings
		temps.append(entry[0])	
		
	min_temp = min(temps)
	
	
	pre_temp = min_temp
	
	if min_temp >= 0:
		temp_idx = int(min_temp / 5)	# split each temperature by every 5 C
		temp_rest = min_temp - temp_idx*5
		if temp_rest >= 2.5:	# for each temperature T, average hum and etx
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
#	tmp_etx_list = []
#	
#	p_temp = []
#	p_etx = []
#	p_etx_std = []		# the standard variance for each etx_avg
	
#	total_etx_avg = 0

	# key = temperature, value = [hum, etx]
	T_hum_etx = {}	
	
	for i in range(0, len(temp_hum_etx_list)):
		# for each <temp, hum, etx> pairs, get <hum, etx> pair for every temperature
#		print "current temp is: " + str(temp_hum_etx_list[i][0])
#		print "-	temp diff is: " + str(temp_hum_etx_list[i][0] - temp_idx*5)
		
		if abs(temp_hum_etx_list[i][0] - temp_idx*5) > 2.5:
			# the end of the previous temperature range
			# the start of next temperature range
			# update temperature index
			temp_idx += 1
#			print "+++++++++++cur temp_idx is: " + str(temp_idx)
			
		else:
			# store hum and etx pairs for this temperature
			if not T_hum_etx.has_key(str(temp_idx*5)):
				T_hum_etx[str(temp_idx*5)] = []
			T_hum_etx[str(temp_idx*5)].append([temp_hum_etx_list[i][1], temp_hum_etx_list[i][2]])
	
	
	for T in T_hum_etx:
		# for each temperature, draw figures about <hum, etx>
		hum_etx_list = T_hum_etx[T]		# get the <hum, etx> pairs
		
		## actuall this should call plot_hum_etx(hum_etx_list, link)
		## however, the path is different, the figures are also slightly different
		
		hum_etx_list.sort()
		pre_hum = hum_etx_list[0][0]
		tmp_etx_list = []
		tmp_hum_list = []
	
		p_hum = []
		p_etx = []
		p_etx_std = []
	
		total_etx_avg = 0
		
#		if link[0] == "10501" and link[1] == "10301":
#			print "\ttemp is: " + T 
#			print "\t" + str(hum_etx_list)
			
		for i in range(0, len(hum_etx_list)):
			
			# for each <hum, etx> pairs, average them for every 1%
			if hum_etx_list[i][0] - pre_hum >= 0.25:
				# Reach 0.5%, compute the average
				avg_etx = 0.0
				avg_hum = 0.0
				etx_std = 0.0
				
				if len(tmp_etx_list) <= 0:
					tmp_hum_list = []
					tmp_etx_list = []
					pre_hum = hum_etx_list[i][0]
					continue
				
				avg_etx = np.mean(tmp_etx_list)
				avg_hum = np.mean(tmp_hum_list)
				etx_std = np.std(tmp_etx_list)
				
				avg_hum_etx.append([avg_hum, avg_etx])
				
				if avg_hum > 0 and avg_etx != 0 :
					p_hum.append(avg_hum)
					p_etx.append(avg_etx)
					p_etx_std.append(etx_std)
					
					total_etx_avg += avg_etx
					
#					if link[0] == "10501" and link[1] == "10301":
#						print "\p_etx is: " + str(p_etx)
		
				tmp_hum_list = []
				tmp_etx_list = []
				pre_hum = hum_etx_list[i][0]
			else:
				tmp_hum_list.append(hum_etx_list[i][0])
				tmp_etx_list.append(hum_etx_list[i][1])
			
		
		## process the last few readings
		
		if len(tmp_etx_list) > 0:
				
			avg_etx = np.mean(tmp_etx_list)
			avg_hum = np.mean(tmp_hum_list)
			etx_std = np.std(tmp_etx_list)
			
			avg_hum_etx.append([avg_hum, avg_etx])
			
			if avg_hum > 0 and avg_etx != 0 :
				p_hum.append(avg_hum)
				p_etx.append(avg_etx)
				p_etx_std.append(etx_std)
				
				total_etx_avg += avg_etx
		
		if len(p_etx) <= 0:
			continue
		
		
		total_etx_avg = int(total_etx_avg/len(p_etx))
		
		# plot figure
		# plot and save the figure of each link, for unified etx and temperature 
		# range
		fig_t = plt.errorbar(p_hum, p_etx, yerr = p_etx_std, fmt='bo')
		plt.ylabel("RSSI / dBm")
		plt.xlabel("Humidity / %")
		
		fig_title = link[0]+ r'$\rightarrow$' + link[1] + ", " + T + " $^\circ$C"
		plt.title(fig_title, loc='center')	# lable for temp_etx main figure	
		
		extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_etx_std))) + " dBm"
		
		extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_max_label = "max_etx: " + str("{0:.2f}".format(np.max(p_etx))) + " dBm"
		
		extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_min_label = "min_etx: " + str("{0:.2f}".format(np.min(p_etx))) + " dBm"

		extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_avg_label = "avg_etx: " + str("{0:.2f}".format(np.mean(p_etx))) + " dBm"

		plt.legend([extra_max, extra_min, extra_avg, extra_std], 
					[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
					, loc='best')

		plt.axis([20, 100, 0, 255])
		plt.xscale('linear')
		
		fig_dir = dir + "_unified\\" + str(int(T) + 100) + "-100_C"
		if not os.path.exists(fig_dir):
			os.makedirs(fig_dir)
		
		# "-56_10011_1_.png"
		plt.savefig(fig_dir + "\\"+ nodes_info[link[0]] + "_" + str(int(T) + 100) + "_" 
						+ str(int(min(p_hum))) + "_"  + str(total_etx_avg) + "_" 
						+ link[0] + "_" + link[1] + ".png")
		plt.clf()
		
		# plot and save figures of each link, use max & min of the etx and temp 
		# as the range
			
		fig_t = plt.errorbar(p_hum, p_etx, yerr = p_etx_std, fmt='bo')
		plt.ylabel("RSSI / dBm")
		plt.xlabel("Humidity / %")
		
		plt.title(fig_title, loc='center')	# lable for temp_etx main figure
		
		extra_std = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_std_label = "avg_std: " + str("{0:.2f}".format(np.mean(p_etx_std))) + " dBm"
		
		extra_max = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_max_label = "max_etx: " + str("{0:.2f}".format(np.max(p_etx))) + " dBm"
		
		extra_min = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_min_label = "min_etx: " + str("{0:.2f}".format(np.min(p_etx))) + " dBm"

		extra_avg = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', 
				linewidth=0)
		extra_avg_label = "avg_etx: " + str("{0:.2f}".format(np.mean(p_etx))) + " dBm"

		plt.legend([extra_max, extra_min, extra_avg, extra_std], 
					[extra_max_label, extra_min_label, extra_avg_label, extra_std_label]
					, loc='best')
		plt.axis([min(p_hum) - 1, max(p_hum) + 1, min(p_etx) - max(p_etx_std) - 0.5, max(p_etx) + max(p_etx_std)+ 0.5])
		
		# draw a line on temperature 35
	#	plt.plot((35, 35), (min(p_etx) - 0.5, max(p_etx) + 0.5), 'b-')
		
		fig_dir = dir + "\\" + str(int(T) + 100) + "-100_C"
		if not os.path.exists(fig_dir):
			os.makedirs(fig_dir)
			
		plt.savefig(fig_dir + "\\"+ nodes_info[link[0]] + "_" + str(int(T) + 100) + "_" 
						+ str(int(min(p_hum))) + "_"  + str(total_etx_avg) + "_" 
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
		
	if not os.path.exists("figures\\etx_hum"):
		os.makedirs("figures\\etx_hum")
	if not os.path.exists("figures\\etx_hum_unified"):
		os.makedirs("figures\\etx_hum_unified")	
		
	if not os.path.exists("figures\\etx_temp"):
		os.makedirs("figures\\etx_temp")
	if not os.path.exists("figures\\etx_temp_unified"):
		os.makedirs("figures\\etx_temp_unified")
	
	if not os.path.exists("figures\\temp_hum_etx"):
		os.makedirs("figures\\temp_hum_etx")
	if not os.path.exists("figures\\temp_hum_etx_unified"):
		os.makedirs("figures\\temp_hum_etx_unified")
	
	
	inf = open("target_nodes_packets\\" + t[0] + "_" + t[1] + ".txt", "r")

	lines = inf.readlines()

	temp_etx = []
	avg_temp_etx = []
	
	hum_etx = []
	avg_hum_etx = []

	temp_hum_etx = []
	
	line_count = 0

	for line in lines:
		line_count += 1
		if line_count > 1:
			s = line.split()
			if len(s) == DATA_LEN :
				if float(s[F_RSSI]) == -97:
					continue
				temp_etx.append([float(s[TEMP]), float(s[ETX])])
				hum_etx.append([float(s[HUM]), float(s[ETX])])
				temp_hum_etx.append([float(s[TEMP]), float(s[HUM]), float(s[ETX])])
	
	plot_temp_etx(temp_etx, t, "figures\\etx_temp")
	plot_hum_etx(hum_etx, t, "figures\\etx_hum")
	
	print t[0] + " -> " + t[1]
	
#	if t[0] == "10011" and t[1] == "1":
		# plot figure for link 10011_1
	plot_temp_hum_etx(temp_hum_etx, t, "figures\\temp_hum_etx")
	
	inf.close()
