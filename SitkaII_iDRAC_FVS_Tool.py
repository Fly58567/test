#===================================================================#
#       Tool Name: SitKaII iDRAC FVS Tool                           #
#         Version: 0.1                                              #
#         Edit by: Fly Li 2018/12/22                                #
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
def check_bmc_selftest():
	'''Check BMC Selftest Result'''

	flag_selftest = False

	ret = Input_CMD_OS("ipmitool mc selftest")
	if(ret == False):
		return False

	for i in ret:
		if("Selftest:" in i and "passed" in i):
			flag_selftest = True

	if(flag_selftest == True):
		Log("Check BMC Selftest Result Pass", FONT_GREEN)
		return True
	else:
		Log("Check BMC Selftest Result Fail", FONT_RED)
		return False
#===============================================================================
def check_bmc_version():
	'''Check BMC FW Version'''

	flag_version = False
	flag_minor1 = False
	flag_minor2 = False
	flag_minor3 = False
	flag_minor4 = False

	ret = Input_CMD_OS("ipmitool mc info")
	if(ret == False):
		return False

	for i in range(len(ret)):
		if("Firmware Revision" in ret[i] and "3.30" in ret[i]):
			flag_version = True
		if("Aux Firmware Rev Info" in ret[i]):
			if("0x00" in ret[i + 1]):
				flag_minor1 = True
			if("0x3c" in ret[i + 2]):
				flag_minor2 = True
			if("0x1e" in ret[i + 3]):
				flag_minor3 = True
			if("0x1e" in ret[i + 4]):
				flag_minor4 = True

	if(flag_version and flag_minor1 and flag_minor2 and flag_minor3 and flag_minor4):
		Log("Check BMC FW Version Pass", FONT_GREEN)
		return True
	else:
		if(flag_version == False):
			Log("Check BMC FW Version Fail (Major Version)", FONT_RED)
		if(flag_minor1 == False):
			Log("Check BMC FW Version Fail (Minor Version 1)", FONT_RED)
		if(flag_minor2 == False):
			Log("Check BMC FW Version Fail (Minor Version 2)", FONT_RED)
		if(flag_minor3 == False):
			Log("Check BMC FW Version Fail (Minor Version 3)", FONT_RED)
		if(flag_minor4 == False):
			Log("Check BMC FW Version Fail (Minor Version 4)", FONT_RED)
		return False
#===============================================================================
def check_bmc_fru():
	'''Check BMC FRU ID 0'''

	global SERVICE_TAG
	global ASSET_TAG

	flag_board_mfg = False
	flag_board_product_name = False
	flag_board_product_number = False

	flag_product_mfg = False
	flag_product_name = False
	flag_product_version = False


	ret = Input_CMD_OS("ipmitool fru print 0")
	if(ret == False):
		return False

	fru_id = 0

	for i in ret:
		if("Board Mfg" in i and "DELL" in i):
			flag_board_mfg = True
		if("Board Product" in i and "PowerEdge R440" in i):
			flag_board_product_name = True
		if("Board Part Number" in i and "0TMPXMX00" in i):
			flag_board_product_number = True

		if("Product Manufacturer" in i and "DELL" in i):
			flag_product_mfg = True
		if("Product Name" in i and "PowerEdge R440" in i):
			flag_product_name = True
		if("Product Version" in i and "01" in i):
			flag_product_version = True




	if(flag_board_mfg and flag_board_product_name and flag_board_product_number and flag_product_mfg and flag_product_name and flag_product_version):
		Log("Check BMC FRU ID 0 Pass", FONT_GREEN)
		return True
	else:
		if(flag_board_mfg == False):
			Log("Check BMC FRU ID %d Fail (Board Mfg)"%(fru_id), FONT_RED)
		if(flag_board_product_name == False):
			Log("Check BMC FRU ID %d Fail (Board Product)"%(fru_id), FONT_RED)
		if(flag_board_product_number == False):
			Log("Check BMC FRU ID %d Fail (Board Part Number)"%(fru_id), FONT_RED)
		if(flag_product_mfg == False):
			Log("Check BMC FRU ID %d Fail (Product Manufacturer)"%(fru_id), FONT_RED)
		if(flag_product_name == False):
			Log("Check BMC FRU ID %d Fail (Product Name)"%(fru_id), FONT_RED)
		if(flag_product_version == False):
			Log("Check BMC FRU ID %d Fail (Product Version)"%(fru_id), FONT_RED)
		return False
#===============================================================================
def check_bmc_chassis():
	'''Check BMC Chassis Status'''

	flag_system_power = False
	flag_system_overload = False
	flag_power_fault = False
	flag_drive_fault = False
	flag_fan_fault = True

	ret = Input_CMD_OS("ipmitool chassis status")
	if(ret == False):
		return False

	for i in ret:
		if("System Power" in i and "on" in i):
			flag_system_power = True
		if("Power Overload" in i and "false" in i):
			flag_system_overload = True
		if("Main Power Fault" in i and "false" in i):
			flag_power_fault = True
		if("Drive Fault" in i and "false" in i):
			flag_drive_fault = True
		if("Cooling/Fan Fault" in i and "false" in i):
			flag_fan_fault = True

	if(flag_system_power and flag_system_overload and flag_power_fault and flag_drive_fault and flag_fan_fault):
		Log("Check BMC Chassis Status Pass", FONT_GREEN)
		return True
	else:
		if(flag_system_power == False):
			Log("Check BMC Chassis Status Fail (System Power)", FONT_RED)
		if(flag_system_overload == False):
			Log("Check BMC Chassis Status Fail (System Overload)", FONT_RED)
		if(flag_power_fault == False):
			Log("Check BMC Chassis Status Fail (Power Fault)", FONT_RED)
		if(flag_drive_fault == False):
			Log("Check BMC Chassis Status Fail (Drive Fault)", FONT_RED)
		if(flag_fan_fault == False):
			Log("Check BMC Chassis Status Fail (Fan Fault)", FONT_RED)
		return False
#===============================================================================
def check_bmc_lan():
	'''Check BMC LAN Status'''

	flag_ip_source = False

	ret = Input_CMD_OS("ipmitool lan print")
	if(ret == False):
		return False

	for i in ret:
		if("IP Address Source" in i and "DHCP Address" in i):
			flag_ip_source = True

	if(flag_ip_source):
		Log("Check BMC LAN Status Pass", FONT_GREEN)
		return True
	else:
		if(flag_ip_source == False):
			Log("Check BMC LAN Status Fail (IP Address Source)", FONT_RED)
		return False
#===============================================================================
def check_bmc_sdr():
	'''Check BMC SDR Information'''

	flag_sdr_status = True

	ret = Input_CMD_OS("ipmitool sdr elist full")
	if(ret == False):
		return False

	for i in ret:
		if(i != ""):
			ret_list = i.split("|")
			for j in range(len(ret_list)):
				ret_list[j] = ret_list[j].strip()

			if(ret_list[2] != "ns" and ret_list[2] != "ok" and ret_list[2] != "lcr" and ret_list[2] != "ucr"):
				flag_sdr_status = False
				break

	if(flag_sdr_status == True):
		Log("Check BMC SDR Information Pass", FONT_GREEN)
		return True
	else:
		Log("Check BMC SDR Information Fail (%s)"%(ret_list[0]), FONT_RED)
		return False
#===============================================================================
def check_bmc_sensor():
	'''Check BMC Sensor Information'''

	flag_sensor_status = True


	ret = Input_CMD_OS("ipmitool sensor")
	if(ret == False):
		return False

	check_list = ["error", "err", "fault", "critical", "fail", "failure"]

	for i in ret:
		if(i != ""):
			ret_list = i.split("|")
			for j in range(len(ret_list)):
				ret_list[j] = ret_list[j].strip()

			for item in check_list:
				if(item in ret_list[3]):
					flag_sensor_status = False
					break
	if(flag_sensor_status):
		Log("Check BMC Sensor Information Pass", FONT_GREEN)
		return True
	else:
		Log("Check BMC Sensor Information Fail (%s)"%(ret_list[0]), FONT_RED)
		return False
#===============================================================================
def check_bmc_sel():
	'''Check BMC SEL Information'''

	flag_sel_overflow = True


	ret = Input_CMD_OS("ipmitool sel")
	if(ret == False):
		return False

	for i in ret:
		if("Overflow" in i and "false" not in i):
			flag_sel_overflow = False
			break
	flag_sel = True

	ret = Input_CMD_OS("ipmitool sel list")
	if(ret == False):
		return False

	check_list = ["error", "err", "fault", "critical", "fail", "failure"]

	index = 0
	for index in range(len(ret)):
		for item in check_list:
			if(item in ret[index]):
				flag_sel = False
				break

	if(flag_sel_overflow and flag_sel):
		Log("Check BMC SEL Information Pass", FONT_GREEN)
		return True
	else:
		if(flag_sel_overflow == False):
			Log("Check BMC SEL Information Fail (SEL Overflow)", FONT_RED)
		if(flag_sel == False):
			Log("Check BMC SEL Information Fail (%s)"%(ret[index]), FONT_RED)
		return False
#===============================================================================
def main():
	global VER
	global DEBUG_MODE
	global FAIL_CONTINUE
	global LOG_DIR
	global LOG_FILE
	global SERVICE_TAG
	global ASSET_TAG

	INIT()

	Banner("SitKaII iDRAC FVS Tool, By Foxconn Luciano Lu, Version: %s"%(VER))

	if(DEBUG_MODE):
		Log("DEBUG_MODE", FONT_WHITE)
	if(FAIL_CONTINUE):
		Log("FAIL_CONTINUE", FONT_WHITE)

	Log("Log Directory: %s"%(LOG_DIR), FONT_WHITE)
	Log("Log File: %s"%(LOG_FILE), FONT_WHITE)

	test_sequence = [
		check_bmc_selftest,
		check_bmc_version,
		check_bmc_fru,
		check_bmc_chassis,
		check_bmc_lan,
		check_bmc_sdr,
		check_bmc_sensor,
		check_bmc_sel,
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
