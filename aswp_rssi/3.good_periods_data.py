'''
** get data from the good periods, when more than 30 nodes are alive
2014-08-07 2014-11-15	100
2015-04-06 2015-05-06	30
2015-05-08 2015-05-10	2
2015-05-21 2015-07-08	48
2015-07-10 2015-09-20	72
2015-09-21 2015-09-24	3
2015-09-27 2015-10-12	15
2015-10-18 2015-12-08	51
2016-02-23 2016-02-23	0

** also get data from 2014-08-02 to 2014-08-04, when many packets are received
due to short sample rate

	2014-08-04 11:51:52.002

** TODO: other periods may also apply.

'''
inf = open("all_data_20140807_rssi_corrected.txt", "r")
inf_p = open("good_periods.txt", "r")

# the list of good periods
# the number indicates the line of the periods in the "good_period.txt"
good_list = [1, 2, 4, 5, 7, 8]	
periods = []	# each element is a tuple [start_p, end_p]

lines = inf_p.readlines()
line_count = 0
for line in lines:
	line_count += 1
	s = line.split()
	if len(s) > 0:
		if line_count in good_list:
			periods.append([s[0], s[1]])

print periods

outf_win1 = open("winter_data1_20141201-20150301.txt", "w")	# winter data
outf_win2 = open("winter_data2_20151201-20160215.txt", "w")	# winter data

lines = inf.readlines()
line_count = 0
periods_index = 0
done = 0
outf = open("good_data" + str(periods_index+1) + "_"
			+ periods[periods_index][0] + "-" + periods[periods_index][1]
			+ ".txt", "w")
for line in lines:
	line_count += 1
	if line_count > 1:
		s = line.split()
		if len(s) > 0:
			if done == 0 and s[0] > periods[periods_index][1] :
				# the end of the previous periods, the start of the next periods.
				print "end period: " + periods[periods_index][1]
				periods_index += 1
				outf.close()
				if periods_index == len(periods):
					# this is the last period, no need to create another file
					print "this is the end of the good periods"
					done = 1
					
				else:
					outf = open("good_data" + str(periods_index+1) + "_"
							+ periods[periods_index][0] + "-" + periods[periods_index][1]
							+ ".txt", "w")
					
					if s[0] >= periods[periods_index][0]:
						outf.writelines(line)
						
			elif done == 0 and s[0] >= periods[periods_index][0]:
				# current time falls in the start_time of a period 
				outf.writelines(line)
				
			if s[0] >= "2014-12-01" and s[0] <= "2015-03-01":
				outf_win1.writelines(line)
			
			if s[0] >= "2015-12-01" and s[0] <= "2016-02-15":
				outf_win2.writelines(line)

inf.close()
outf_win1.close()
outf_win2.close()
	