import os

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