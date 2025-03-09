#===================================================================#
#       Tool Name: SitKaII HWCHK FVS Tool                           #
#         Version: 0.1                                              #
#         Edit by: Luciano Lu 2018/12/22                            #
#===================================================================#
import sys
import datetime
import subprocess
import os
import time
import ctypes

global VER
VER = "0.1"

global LOG_FILE
LOG_FILE = "test.log"

global ROOT_DIR
ROOT_DIR = os.getcwd()

global LOG_DIR
LOG_DIR = os.path.join(ROOT_DIR, "Log")

global DEBUG_MODE
DEBUG_MODE = True

global FAIL_CONTINUE
FAIL_CONTINUE = False

global CMOS_YEAR
CMOS_YEAR = "2019"


FONT_NONE   = 0
FONT_WHITE  = 1
FONT_RED    = 2
FONT_GREEN  = 3
FONT_YELLOW = 4

PASS_BANNER = """
########     ###     ######   ######     #### ####
##     ##   ## ##   ##    ## ##    ##    #### ####
##     ##  ##   ##  ##       ##          #### ####
########  ##     ##  ######   ######      ##   ##
##        #########       ##       ##
##        ##     ## ##    ## ##    ##    #### ####
##        ##     ##  ######   ######     #### ####
"""

FAIL_BANNER = """
########    ###    #### ##          #### ####
##         ## ##    ##  ##          #### ####
##        ##   ##   ##  ##          #### ####
######   ##     ##  ##  ##           ##   ##
##       #########  ##  ##
##       ##     ##  ##  ##          #### ####
##       ##     ## #### ########    #### ####
"""
#===============================================================================
def INIT():
	global LOG_FILE
	global LOG_DIR
	global ASSET_TAG
	global SERVICE_TAG

	cmd = "ifconfig -a eth0 | grep HWaddr | awk '{print $5}'"
	sled_mac = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, universal_newlines = True).communicate()[0].split("\n")[0]

	cmd = "ifconfig eth0 | grep \"inet addr:\""
	sled_ip = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, universal_newlines = True).communicate()[0].split("\n")[0].strip().split()[1].split(":")[1]

	f = open("/usr/local/scan/%s/scan.dat"%(sled_mac), "r")
	ret1 = f.readlines()
	for i in range(len(ret1)):
		ret1[i] = ret1[i].strip()
	f.close()

	sled_ppid = ""

	for i in ret1:
		if("PPID" in i):
			sled_ppid = i.split("=", 1)[1].strip()
		if("Asset Tag" in i):
			ASSET_TAG = i.split("=", 1)[1].strip()
		if("Service Tag" in i):
			SERVICE_TAG = i.split("=", 1)[1].strip()

	LOG_DIR = os.path.join("/usr/local/scan/%s"%(sled_ppid))

	if(os.path.isdir(LOG_DIR) == False):
		os.mkdir(LOG_DIR)

	LOG_FILE = "LOG_%s_%s.txt"%(os.path.basename(__file__).split(".")[0], datetime.datetime.strftime(datetime.datetime.now(), "%m%d-%H%M"))
#===============================================================================
def Banner(msg):
	line_0 = "#" + "="*78 + "#"
	line_1 = "#" + " "*78 + "#"
	tmp_str = "#" + msg.center(78) + "#"

	if(sys.platform == "win32"):
		ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x08)
		print("")
		print(line_0)
		print(line_1)
		print(tmp_str)
		print(line_1)
		print(line_0)
		print("")
		ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x04)
	else:
		print("")
		print("\033[35;1m%s\033[0m"%(line_0))
		print("\033[35;1m%s\033[0m"%(line_1))
		print("\033[35;1m%s\033[0m"%(tmp_str))
		print("\033[35;1m%s\033[0m"%(line_1))
		print("\033[35;1m%s\033[0m"%(line_0))
		print("")
#===============================================================================
def Log(msg, color = FONT_WHITE):
	tmp = "[%s] %s\n"%(datetime.datetime.strftime(datetime.datetime.now(), "%y/%m/%d %H:%M:%S"), msg)

	try:
		f = open(os.path.join(LOG_DIR, LOG_FILE), "a")
		f.write(tmp)
		f.close()
	except:
		print("Logging Error!!")
		return

	tmp = tmp[:-1]

	if(color == FONT_RED):
		if(sys.platform == "win32"):
			ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x04 | 0x08)
			print(tmp)
			ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x04)
		else:
			print("\033[31;1m%s\033[0m"%(tmp))
	elif(color == FONT_GREEN):
		if(sys.platform == "win32"):
			ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x02 | 0x08)
			print(tmp)
			ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x04)
		else:
			print("\033[32;1m%s\033[0m"%(tmp))
	elif(color == FONT_YELLOW):
		if(sys.platform == "win32"):
			ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x02 | 0x04 | 0x08)
			print(tmp)
			ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x04)
		else:
			print("\033[33;1m%s\033[0m"%(tmp))
	elif(color == FONT_NONE):
		pass
	else:
		try:
			print(tmp)
		except:
			print("Logging Error!!")
#===============================================================================
def Show_Pass():
	if(sys.platform == "win32"):
		ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x02 | 0x08)
		print(PASS_BANNER)
		ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x04)
	else:
		print("\033[32;1m%s\033[0m"%(PASS_BANNER))

	Log("Log File: %s"%(os.path.join(LOG_DIR, LOG_FILE)), FONT_GREEN)
	Log("PASS", FONT_GREEN)
	sys.exit(0)
#===============================================================================
def Show_Fail(error_msg):
	if(sys.platform == "win32"):
		ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x04 | 0x08)
		print(FAIL_BANNER)
		ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x01 | 0x02 | 0x04)
	else:
		print("\033[31;1m%s\033[0m"%(FAIL_BANNER))

	Log("Log File: %s"%(os.path.join(LOG_DIR, LOG_FILE)), FONT_RED)
	Log("Error Message: %s"%(error_msg), FONT_RED)
	Log("FAIL", FONT_RED)
	sys.exit(-1)
#===============================================================================
def Input_CMD_OS(cmd):
	Log("Input OS Command: %s"%(cmd), FONT_YELLOW)

	try:
		ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell = True, universal_newlines = True).communicate()[0].splitlines()
	except:
		Log("Input OS Command Fail (%s)"%(cmd), FONT_RED)
		return False

	for i in range(len(ret)):
		ret[i] = ret[i].strip()
		if(DEBUG_MODE):
			Log("ret[%02d] %s"%(i, ret[i]), FONT_WHITE)

	return ret
#===============================================================================
def Input_CMD_OS_1(cmd):
	Log("Input OS Command: %s"%(cmd), FONT_WHITE)

	ret = []

	try:
		process = subprocess.Popen(cmd, shell = True, universal_newlines = True, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
		while(process.poll() == None):
			for i in iter(lambda: process.stdout.readline(), ""):
				Log(i, FONT_WHITE)
				ret.append(i)

		process.communicate()
	except:
		Log("Input Command Fail (%s)"%(cmd), FONT_RED)
		return False

	if(process.returncode == 0):
		return ret
	else:
		Log("Input Command Fail (%s)"%(cmd), FONT_RED)
		return False
#===============================================================================
class Dimm:
	def __init__(self, locator):
		self.locator = locator
		self.manufacturer = ""
		self.size = ""
		self.width = ""
		self.speed = ""
		self.part_number = ""
		self.serial_number = ""
		self.current_speed = ""
		self.current_voltage = ""
#===============================================================================
def check_smbios_bios():
	'''Check BIOS Information (SMBIOS)'''

	flag_vendor = False
	flag_version = False

	ret = Input_CMD_OS("dmidecode -t 0")
	if(ret == False):
		return False

	for i in ret:
		if("Vendor:" in i and "Dell Inc." in i):
			flag_vendor = True
		if("Version:" in i and "1.7.24" in i):
			flag_version = True

	if(flag_vendor and flag_version):
		Log("check_smbios_bios Pass", FONT_GREEN)
		return True
	else:
		if(flag_vendor == False):
			Log("check_smbios_bios Fail (Vendor)", FONT_RED)
		if(flag_version == False):
			Log("check_smbios_bios Fail (Version)", FONT_RED)
		return False
#===============================================================================
def check_smbios_system():
	'''Check System Information (SMBIOS)'''

	global SERVICE_TAG

	flag_manufacturer = False
	flag_product = False


	ret = Input_CMD_OS("dmidecode -t 1")
	if(ret == False):
		return False

	for i in range(len(ret)):
		if("Manufacturer:" in ret[i] and "Dell Inc." in ret[i]):
			flag_manufacturer = True
		if("Product Name:" in ret[i] and "PowerEdge R440" in ret[i]):
			flag_product = True

	if(flag_manufacturer and flag_product):
		Log("check_smbios_system Pass", FONT_GREEN)
		return True
	else:
		if(flag_manufacturer == False):
			Log("check_smbios_system Fail (Manufacturer)", FONT_RED)
		if(flag_product == False):
			Log("check_smbios_system Fail (Product Name)", FONT_RED)
		return False
#===============================================================================
def check_smbios_baseboard():
	'''Check Baseboard Information (SMBIOS)'''

	flag_manufacturer = False
	flag_product = False
	flag_version = False


	ret = Input_CMD_OS("dmidecode -t 2")
	if(ret == False):
		return False

	for i in ret:
		if("Manufacturer:" in i and "Dell Inc." in i):
			flag_manufacturer = True
		if("Product Name:" in i and "0TMPXM" in i):
			flag_product = True
		if("Version:" in i and "X00" in i):
			flag_version = True


	if(flag_manufacturer and flag_product and flag_version):
		Log("check_smbios_baseboard Pass", FONT_GREEN)
		return True
	else:
		if(flag_manufacturer == False):
			Log("check_smbios_baseboard Fail (Manufacturer)", FONT_RED)
		if(flag_product == False):
			Log("check_smbios_baseboard Fail (Product Name)", FONT_RED)
		if(flag_version == False):
			Log("check_smbios_baseboard Fail (Version)", FONT_RED)
		return False
#===============================================================================
def check_smbios_chassis():
	'''Check Chassis Information (SMBIOS)'''

	flag_manufacturer = False
	flag_type = False


	flag_asset_tag = False
	flag_service_tag = False

	ret = Input_CMD_OS("dmidecode -t 3")
	if(ret == False):
		return False

	for i in ret:
		if("Manufacturer:" in i and "Dell Inc." in i):
			flag_manufacturer = True
		if("Type:" in i and "Rack Mount Chassis" in i):
			flag_type = True


	if(flag_manufacturer and flag_type):
		Log("check_smbios_chassis Pass", FONT_GREEN)
		return True
	else:
		if(flag_manufacturer == False):
			Log("check_smbios_chassis Fail (Manufacturer)", FONT_RED)
		if(flag_type == False):
			Log("check_smbios_chassis Fail (Type)", FONT_RED)
		return False
#===============================================================================
def check_cpu_info():
	'''Check CPU Information'''

	flag_manufacturer = False
	flag_version = False
	flag_speed = False
	flag_core = False
	flag_thread = False

	ret = Input_CMD_OS("dmidecode -t 4")
	if(ret == False):
		return False

	for i in range(len(ret)):
		if("Manufacturer:" in ret[i] and "Intel" in ret[i]):
			flag_manufacturer = True
		if("Version:" in ret[i] and "Intel(R) Xeon(R) Bronze 3104 CPU @ 1.70GHz" in ret[i]):
			flag_version = True
		if("Current Speed:" in ret[i] and "1700" in ret[i]):
			flag_speed = True
		if("Core Count:" in ret[i] and "6" in ret[i]):
			flag_core = True
		if("Thread Count:" in ret[i] and "6" in ret[i]):
			flag_thread = True

	ret = Input_CMD_OS("lscpu")
	if(ret == False):
		return False

	flag_socket = False
	flag_family = False
	flag_model = False
	flag_stepping = False
	flag_L1d = False
	flag_L1i = False
	flag_L2 = False
	flag_L3 = False

	for i in range(len(ret)):
		if("Socket(s):" in ret[i] and "2" in ret[i]):
			flag_socket = True
		if("CPU family:" in ret[i] and "6" in ret[i]):
			flag_family = True
		if("Model:" in ret[i] and "85" in ret[i]):
			flag_model = True
		if("Stepping:" in ret[i] and "4" in ret[i]):
			flag_stepping = True
		if("L1d cache:" in ret[i] and "32K" in ret[i]):
			flag_L1d = True
		if("L1i cache:" in ret[i] and "32K" in ret[i]):
			flag_L1i = True
		if("L2 cache:" in ret[i] and "1024K" in ret[i]):
			flag_L2 = True
		if("L3 cache:" in ret[i] and "8448K" in ret[i]):
			flag_L3 = True

	if(flag_manufacturer and flag_version and flag_speed and flag_core and flag_thread and flag_socket and flag_family and flag_model and flag_stepping and flag_L1d and flag_L1i and flag_L2 and flag_L3):
		Log("check_cpu_info Pass", FONT_GREEN)
		return True
	else:
		if(flag_manufacturer == False):
			Log("check_cpu_info Fail (Manufacturer)", FONT_RED)
		if(flag_version == False):
			Log("check_cpu_info Fail (Version)", FONT_RED)
		if(flag_speed == False):
			Log("check_cpu_info Fail (Speed)", FONT_RED)
		if(flag_core == False):
			Log("check_cpu_info Fail (Core)", FONT_RED)
		if(flag_thread == False):
			Log("check_cpu_info Fail (Thread)", FONT_RED)
		if(flag_socket == False):
			Log("check_cpu_info Fail (Socket)", FONT_RED)
		if(flag_family == False):
			Log("check_cpu_info Fail (Family)", FONT_RED)
		if(flag_model == False):
			Log("check_cpu_info Fail (Model)", FONT_RED)
		if(flag_stepping == False):
			Log("check_cpu_info Fail (Stepping)", FONT_RED)
		if(flag_L1d == False):
			Log("check_cpu_info Fail (L1d Cache)", FONT_RED)
		if(flag_L1i == False):
			Log("check_cpu_info Fail (L1i Cache)", FONT_RED)
		if(flag_L2 == False):
			Log("check_cpu_info Fail (L2 Cache)", FONT_RED)
		if(flag_L3 == False):
			Log("check_cpu_info Fail (L3 Cache)", FONT_RED)
		return False
#===============================================================================
def check_memory_info():
	'''Check Memory Information'''

	flag_total_size = False
	memory_size = 0


	ret = Input_CMD_OS("cat /proc/meminfo")
	if(ret == False):
		return False

	for i in range(len(ret)):
		if("MemTotal" in ret[i]):
			memory_size = int(ret[i].split()[1])

	if(memory_size > 16000000):
		flag_total_size = True

	ret = Input_CMD_OS("dmidecode -t 17")
	if(ret == False):
		return False

	dimm_locator_list = ["A1", "B1"]
	dimm_list = []

	for i in dimm_locator_list:
		for index in range(len(ret)):
			if("Locator:" in ret[index]):
				dimm_index = ret[index].split(":")[1].strip()
				if(i == dimm_index):
					dimm_list.append(Dimm(i))
					dimm_list[-1].manufacturer = ret[index + 5].split(None, 1)[1]
					dimm_list[-1].size = ret[index - 3].split(None, 1)[1]
					dimm_list[-1].width = ret[index - 5].split(None, 2)[2]
					dimm_list[-1].speed = ret[index + 4].split(None, 1)[1]
					dimm_list[-1].part_number = ret[index + 8].split(None, 2)[2]
					dimm_list[-1].serial_number = ret[index + 6].split(None, 2)[2]
					dimm_list[-1].current_speed = ret[index + 10].split(None, 3)[3]
					dimm_list[-1].current_voltage = ret[index + 13].split(None, 2)[2]

	for i in dimm_list:
		Log("===================================================", FONT_YELLOW)
		Log("DIMM %s Manufacturer: %s"%(i.locator, i.manufacturer), FONT_YELLOW)
		Log("DIMM %s Size: %s"%(i.locator, i.size), FONT_YELLOW)
		Log("DIMM %s Total Width: %s"%(i.locator, i.width), FONT_YELLOW)
		Log("DIMM %s Speed: %s"%(i.locator, i.speed), FONT_YELLOW)
		Log("DIMM %s Part Number: %s"%(i.locator, i.part_number), FONT_YELLOW)
		Log("DIMM %s Serial Number: %s"%(i.locator, i.serial_number), FONT_YELLOW)
		Log("DIMM %s Current Speed: %s"%(i.locator, i.current_speed), FONT_YELLOW)
		Log("DIMM %s Current Voltage: %s"%(i.locator, i.current_voltage), FONT_YELLOW)
		Log("===================================================", FONT_YELLOW)

	flag_same_pn = True

	temp_pn = dimm_list[0].part_number
	for i in dimm_list:
		if(i.part_number != temp_pn):
			flag_same_pn = False

	for i in dimm_list:
		flag_manufacturer = False
		flag_size = False
		flag_width = False
		flag_speed = False
		flag_part_number = False
		flag_current_speed = False
		flag_current_voltage = False

		if(i.manufacturer in ["00CE063200CE"]):
			flag_manufacturer = True
		if(i.size == "8192 MB"):
			flag_size = True
		if(i.width == "72 bits"):
			flag_width = True
		if(i.speed == "2666 MHz"):
			flag_speed = True
		if(i.part_number in ["M393A1K43BB1-CTD"]):
			flag_part_number = True
		if(i.current_speed == "2133 MHz"):
			flag_current_speed = True
		if(i.current_voltage == "1.2 V"):
			flag_current_voltage = True

		if(flag_manufacturer and flag_size and flag_width and flag_speed and flag_part_number and flag_current_speed and flag_current_voltage):
			Log("Check DIMM%s Pass"%(i.locator), FONT_GREEN)
			continue
		else:
			Log("Check DIMM%s Fail"%(i.locator), FONT_RED)
			break

	if(flag_total_size and flag_same_pn and flag_manufacturer and flag_size and flag_width and flag_speed and flag_part_number and flag_current_speed and flag_current_voltage):
		Log("check_memory_info Pass", FONT_GREEN)
		return True
	else:
		if(flag_total_size == False):
			Log("check_memory_info Fail (Total Size)", FONT_RED)
		if(flag_same_pn == False):
			Log("check_memory_info Fail (Same Part Number)", FONT_RED)
		if(flag_manufacturer == False):
			Log("check_memory_info Fail (DIMM %s Manufacturer)"%(i.locator), FONT_RED)
		if(flag_size == False):
			Log("check_memory_info Fail (DIMM %s Size)"%(i.locator), FONT_RED)
		if(flag_width == False):
			Log("check_memory_info Fail (DIMM %s Total Width)"%(i.locator), FONT_RED)
		if(flag_speed == False):
			Log("check_memory_info Fail (DIMM %s Speed)"%(i.locator), FONT_RED)
		if(flag_part_number == False):
			Log("check_memory_info Fail (DIMM %s Part Number)"%(i.locator), FONT_RED)
		if(flag_current_speed == False):
			Log("check_memory_info Fail (DIMM %s Current Speed)"%(i.locator), FONT_RED)
		if(flag_current_voltage == False):
			Log("check_memory_info Fail (DIMM %s Current Voltage)"%(i.locator), FONT_RED)
		return False
#===============================================================================
def check_pcie_perc():
	'''Check Dell PERC H330 PCIe Information'''

	flag_id = False
	flag_status = False

	ret = Input_CMD_OS("lspci -s 01:00.0 -vv -x")
	if(ret == False):
		return False

	for i in range(len(ret)):
		if("00: 00 10 5f 00" in ret[i]):
			flag_id = True
		if("LnkSta:" in ret[i] and "Speed 8GT/s, Width x8" in ret[i]):
			flag_status = True

	if(flag_id and flag_status):
		Log("check_pcie_perc Pass", FONT_GREEN)
		return True
	else:
		if(flag_id == False):
			Log("check_pcie_perc Fail (VID/DID)", FONT_RED)
		if(flag_status == False):
			Log("check_pcie_perc Fail (Link Speed/Width)", FONT_RED)
		return False
#===============================================================================
def Check_Sensor():
	'''Check System Sensor (racadm)'''

	flag_cpu1_temp = False
	flag_cpu2_temp = False
	flag_cmos = False


	ret = Input_CMD_OS("racadm getsensorinfo")
	if(ret == False):
		return False

	for i in ret:
		if("CPU1 Temp" in i and "Ok" in i):
			flag_cpu1_temp = True
		if("CPU2 Temp" in i and "Ok" in i):
			flag_cpu2_temp = True
		if("System Board CMOS Battery" in i and "Ok" in i and "Present" in i):
			flag_cmos = True


	if(flag_cpu1_temp and flag_cpu2_temp and flag_cmos):
		Log("Check_Sensor Pass", FONT_GREEN)
		return True
	else:
		if(flag_cpu1_temp == False):
			Log("Check_Sensor Fail (CPU1 Temperature)", FONT_RED)
		if(flag_cpu2_temp == False):
			Log("Check_Sensor Fail (CPU2 Temperature)", FONT_RED)
		if(flag_cmos == False):
			Log("Check_Sensor Fail (CMOS)", FONT_RED)
		return False
#===============================================================================
def Check_Intrusion():
	'''Check System Board Intrusion'''
	
	flag = False
	
	ret = Input_CMD_OS("racadm getsensorinfo")
	if(ret == False):
		return False
	for i in ret:
		if("System Board Intrusion" in i and "Closed" in i):
			flag = True
	if(flag):
		Log("Check_Intrusion Pass", FONT_GREEN)
		return True
	else:
		Log("Check_Intrusion Fail", FONT_RED)
		return False
#===============================================================================
def Check_Fan():
	'''Check Fan Speed'''
	fan_list = [
		"Fan1A",
		"Fan1B",
		"Fan2A",
		"Fan2B",
		"Fan3A",
		"Fan3B",
		"Fan4A",
		"Fan4B",
		"Fan5A",
		"Fan5B",
		"Fan6A",
		"Fan6B"		
	]
	
	fan_min = 2500
	fan_max = 6000
	
	ret = Input_CMD_OS("racadm getsensorinfo")
	if(ret == False):
		return False
		
	for fan in fan_list:
		flag = False
		status = False
		speed = False

		for i in range(len(ret)):
			if("System Board %s"%fan in ret[i]):
				flag = True
				fan_speed = int(ret[i].split()[4][:-3].strip())
				Log("%s speed is %sRPM"%(fan, fan_speed), FONT_YELLOW)
				if(ret[i].split()[3].strip() == "Ok"):
					status = True
				if(fan_min < fan_speed < fan_max):
					speed = True
					

		if(flag and status and speed):
			Log("Check_Fan %s Pass"%fan, FONT_GREEN)
			continue
		else:
			if(flag == False):
				Log("Check_Fan %s(present) Fail"%fan, FONT_RED)
			if(status == False):
				Log("Check_Fan %s(status) Fail"%fan, FONT_RED)
			if(speed == False):
				Log("Check_Fan %s(speed) Fail"%fan, FONT_RED)
			break
			
	if(flag and status and speed):
		Log("Check_Fan Pass", FONT_GREEN)
		return True
	else:
		if(flag == False):
			Log("Check_Fan(present) Fail", FONT_RED)
		if(status == False):
			Log("Check_Fan(status) Fail", FONT_RED)
		if(speed == False):
			Log("Check_Fan(speed) Fail", FONT_RED)
		return False
#===============================================================================			
def Check_NIC_Info():
	'''Check NIC Status'''

	flag_eth0_mode = False
	flag_eth0_port = False
	flag_eth0_link = False
	flag_eth0_speed = False

	Log("Check eth0 Status", FONT_YELLOW)
	ret = Input_CMD_OS("ethtool eth0")
	if(ret == False):
		return False

	for i in ret:
		if("Supported link modes:" in i and "10baseT/Full" in i):
			flag_eth0_mode = True
		if("Supported ports:" in i and "TP" in i):
			flag_eth0_port = True
		if("Link detected:" in i and "yes" in i):
			flag_eth0_link = True
		if("Speed:" in i and "1000Mb/s" in i):
			flag_eth0_speed = True


	if(flag_eth0_mode and flag_eth0_port and flag_eth0_link and flag_eth0_speed):
		Log("Check_NIC_Info Pass", FONT_GREEN)
		return True
	else:
		if(flag_eth0_mode == False):
			Log("Check_NIC_Info Fail (eth0 Link Mode)", FONT_RED)
		if(flag_eth0_port == False):
			Log("Check_NIC_Info Fail (eth0 Link Port)", FONT_RED)
		if(flag_eth0_link == False):
			Log("Check_NIC_Info Fail (eth0 Link Link)", FONT_RED)
		if(flag_eth0_speed == False):
			Log("Check_NIC_Info Fail (eth0 Link Speed)", FONT_RED)
		return False
#===============================================================================
def Check_CMOS_Date():
	'''Check CMOS DATE'''

	global CMOS_YEAR

	flag = False

	ret = Input_CMD_OS("date -u")
	if(ret == False):
		return False

	year = ""
	for i in ret:
		if("UTC" in i):
			Log("CMOS DATE: %s"%(i), FONT_YELLOW)
			year = i.split()[5].strip()
			if(year == CMOS_YEAR):
				flag = True
			break

	if(flag):
		Log("Check_CMOS_Date Pass", FONT_GREEN)
		return True
	else:
		Log("Check_CMOS_Date Fail", FONT_RED)
		return False
#===============================================================================
def Check_PERC_Info():
	'''Check PERC Information via perccli'''

	flag_product = False
	flag_fw = False
	flag_mode = False

	ret = Input_CMD_OS("/opt/MegaRAID/perccli/perccli64 /c0 show")
	if(ret == False):
		return False

	for i in ret:
		if("Product Name" in i and "PERC H330 Adapter" in i):
			flag_product = True
		if("FW Package Build" in i and "25.5.3.0005" in i):
			flag_fw = True
		if("Current Personality" in i and "HBA-Mode" in i):
			flag_mode = True

	if(flag_product and flag_fw and flag_mode):
		Log("Check_PERC_Info Pass", FONT_GREEN)
		return True
	else:
		if(flag_product == False):
			Log("Check_PERC_Info Fail (Product Name)", FONT_RED)
		if(flag_fw == False):
			Log("Check_PERC_Info Fail (FW Version)", FONT_RED)
		if(flag_mode == False):
			Log("Check_PERC_Info Fail (Mode)", FONT_RED)
		return False
#===============================================================================
def Check_Nvme_SSD():
	'''Check Nvme SSD information'''
	nvme_list = ["nvme%sn1"%i for i in range(0,4)]
	
	ret = Input_CMD_OS("./nvme list")
	if(ret == False):
		return False
	
	for nvme in nvme_list:
		present = False
		size = False
		fw = False
		for i in ret:
			if("/dev/%s"%nvme in i):
				present = True
				if("1.60  TB" in i):
					size = True
				if("VDV1DB22" in i):
					fw = True
		if(present and size and fw):
			Log("Check_Nvme_SSD %s Pass"%nvme, FONT_GREEN)
			continue
		else:
			if(present == False):
				Log("Check_Nvme_SSD %s(present) Fail"%nvme, FONT_RED)
			if(size == False):
				Log("Check_Nvme_SSD %s(size) Fail"%nvme, FONT_RED)
			if(fw == False):
				Log("Check_Nvme_SSD %s(fw) Fail"%nvme, FONT_RED)
			break
	if(present and size and fw):
		Log("Check_Nvme_SSD Pass", FONT_GREEN)
		return True
	else:
		if(present == False):
			Log("Check_Nvme_SSD Fail", FONT_RED)
		if(size == False):
			Log("Check_Nvme_SSD Fail", FONT_RED)
		if(fw == False):
			Log("Check_Nvme_SSD %s(fw) Fail"%nvme, FONT_RED)
		return False
#===============================================================================
def Check_OTG():
	'''Check OTG information'''
	flag = False
	cmd = "ifconfig -a | grep \"idrac\" | awk '{print $5}'"
	ret = Input_CMD_OS(cmd)
	if(ret == False):
		return False
	for i in ret:
		if(i != "" and len(i) == 17):
			Log("OTG mac is %s"%i, FONT_YELLOW)
			flag = True
	if(flag):
		Log("Check OTG Pass", FONT_GREEN)
		return True
	else:
		Log("Check OTG Fail", FONT_RED)
		return False
#===============================================================================
def Check_PD_Info_2P5():
	'''Check 2.5" eSATA Physical Disk Information'''

	hdd_list = ["sda"]

	for hdd in hdd_list:
		Log("Check PD %s Information"%(hdd), FONT_YELLOW)
		ret = Input_CMD_OS("smartctl -i -H /dev/%s"%(hdd))
		if(ret == False):
			return False

		flag_smart = False
		flag_model = False
		flag_fw = False
		flag_size = False
		flag_speed = False

		for i in ret:
			if("SMART overall-health self-assessment test result:" in i and "PASSED" in i):
				flag_smart = True
			if("Device Model:" in i and "SSDSC2BB120G7R" in i):
				flag_model = True
			if("Firmware Version:" in i and "N201DL41" in i):
				flag_fw = True
			if("User Capacity:" in i and "120 GB" in i):
				flag_size = True
			if("SATA Version is:" in i and "current: 6.0 Gb/s" in i):
				flag_speed = True


		if(flag_smart and flag_model and flag_fw and flag_size and flag_speed):
			Log("Check PD %s Information Pass"%(hdd), FONT_GREEN)
			continue
		else:
			Log("Check PD %s Information Fail"%(hdd), FONT_RED)
			break

	if(flag_smart and flag_model and flag_fw and flag_size and flag_speed):
		Log("Check_PD_Info_2P5 Pass", FONT_GREEN)
		return True
	else:
		if(flag_smart == False):
			Log("Check_PD_Info_2P5 Fail (PD %s SMART)"%(hdd), FONT_RED)
		if(flag_model == False):
			Log("Check_PD_Info_2P5 Fail (PD %s Model)"%(hdd), FONT_RED)
		if(flag_fw == False):
			Log("Check_PD_Info_2P5 Fail (PD %s FW)"%(hdd), FONT_RED)
		if(flag_size == False):
			Log("Check_PD_Info_2P5 Fail (PD %s Size)"%(hdd), FONT_RED)
		if(flag_speed == False):
			Log("Check_PD_Info_2P5 Fail (PD %s Speed)"%(hdd), FONT_RED)
		return False
#===============================================================================

def main():
	global VER
	global DEBUG_MODE
	global FAIL_CONTINUE
	global LOG_DIR
	global LOG_FILE

	INIT()

	Banner("SitKaII HWCHK Tool, By Foxconn Luciano Lu, Version: %s"%(VER))

	if(DEBUG_MODE):
		Log("DEBUG_MODE", FONT_WHITE)
	if(FAIL_CONTINUE):
		Log("FAIL_CONTINUE", FONT_WHITE)

	Log("Log Directory: %s"%(LOG_DIR), FONT_WHITE)
	Log("Log File: %s"%(LOG_FILE), FONT_WHITE)

	test_sequence = [
		check_smbios_bios,
		check_smbios_system,
		check_smbios_baseboard,
		check_smbios_chassis,
		check_cpu_info,
		check_memory_info,
		Check_Sensor,
		Check_Intrusion,
		Check_Fan,
		Check_CMOS_Date,
		Check_NIC_Info,
		#Check_Nvme_SSD,
		Check_OTG,
 		Check_PD_Info_2P5,
	]

	test_result = True
	result_msg = []

	test_start = datetime.datetime.now()
	Log("Test Start...", FONT_YELLOW)
	for test_item in test_sequence:
		Log("="*58, FONT_NONE)
		Banner(test_item.__doc__)
		Log("Test Item: %s (%s)"%(test_item.__doc__, test_item.__name__), FONT_YELLOW)
		time.sleep(1)
		if(test_item() == False):
			test_result = False
			result_msg.append((test_item.__name__, False))
			if(FAIL_CONTINUE):
				raw_input("%s Fail!! Press ENTER to Continue..."%(test_item.__doc__))
			else:
				break
		else:
			result_msg.append((test_item.__name__, True))
		time.sleep(1)
		Log("="*58, FONT_NONE)
	Log("Test End...", FONT_YELLOW)
	test_end = datetime.datetime.now()

	print("")
	Log("Test Start: %s"%(str(test_start)), FONT_YELLOW)
	Log("Test End:   %s"%(str(test_end)), FONT_YELLOW)
	Log("Test Time:  %s"%(str(test_end - test_start)), FONT_YELLOW)
	print("")
	for (item_name, result) in result_msg:
		if(result):
			msg = item_name.ljust(52, "-") + "[PASS]"
			Log(msg, FONT_GREEN)
		else:
			msg = item_name.ljust(52, "-") + "[FAIL]"
			Log(msg, FONT_RED)
	print("")

	if(test_result):
		Show_Pass()
	else:
		Show_Fail("%s Fail"%(test_item.__doc__))
#===============================================================================
if(__name__ == "__main__"):
	main()
	sys.exit(0)
