#===================================================================#
#       Tool Name: SitKaII 2.5 MB FW FVS Tool                       #
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

global BIOS_VER
BIOS_VER = "1.7.24"

global CPLD_VER
CPLD_VER = "1.0.5"

global IDRAC_VER
IDRAC_VER = "3.30.30.30"

global IDRAC_BUILD
IDRAC_BUILD = "60"

global BP_VER
BP_VER = "4.28"

global PERC_VER
PERC_VER = "25.5.3.0005"

global NIC_VER
NIC_VER = "20.6.16"

global PSU_VER
PSU_VER = "00.0C.7D"

global NCNFF
NCNFF = "00.30.47"

global IDRAC_DUP
IDRAC_DUP = "iDRAC-with-Lifecycle-Controller_Firmware_6X8V5_LN_3.30.30.30_A00.BIN"



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
def Check_BIOS_VER():
	'''Check BIOS Version'''

	global BIOS_VER

	flag = False
	bios = ""

	ret = Input_CMD_OS("dmidecode -t 0")
	if(ret == False):
		return False

	for i in ret:
		if("Version:" in i and BIOS_VER in i):
			Log(i, FONT_YELLOW)
			bios = i.split()[1]
			Log("BIOS Version: %s"%(bios), FONT_YELLOW)
			flag = True
			break

	if(flag):
		Log("Check_BIOS_VER Pass", FONT_GREEN)
		return True
	else:
		Log("Check_BIOS_VER Fail", FONT_RED)
		return True
#===============================================================================
def Check_CPLD_VER():
	'''Check CPLD Version'''

	global CPLD_VER

	flag = False
	cpld = ""

	ret = Input_CMD_OS("ipmitool raw 0x30 0x33")
	if(ret == False):
		return False

	cpld = "%d.%d.%d"%(int(ret[0].split()[0]), int(ret[0].split()[1]), int(ret[0].split()[2]))
	if(cpld == CPLD_VER):
		flag = True

	Log("CPLD Version: %s"%(cpld), FONT_YELLOW)

	if(flag):
		Log("Check_CPLD_VER Pass", FONT_GREEN)
		return True
	else:
		Log("Check_CPLD_VER Fail", FONT_RED)
		return False
#===============================================================================
def Check_iDRAC_VER():
	'''Check iDRAC Version'''
	
	global IDRAC_VER
	global IDRAC_DUP
	
	flag_ver = False
	flag_build = False

	ret = Input_CMD_OS("racadm getsysinfo")
	if(ret == False):
		return False

	for i in ret:
		if("Firmware Version" in i and IDRAC_VER in i):
			Log(i, FONT_YELLOW)
			flag_ver = True
		if("Firmware Build" in i and IDRAC_BUILD in i):
			Log(i, FONT_YELLOW)
			flag_build = True

	if(flag_ver and flag_build):
		Log("Check_iDRAC_VER Pass", FONT_GREEN)
		return True
	else:
		if(flag_ver == False):
			Log("Check_iDRAC_VER Fail", FONT_RED)
		if(flag_build == False):
			Log("Check_Firmware Build Fail", FONT_RED)	
		return False

	#	Log("Update iDRAC to 3.30.30.30", FONT_YELLOW)
	#	ret = Input_CMD_OS("./%s -q -f"%IDRAC_DUP)
	#	if(ret == False):
	#		Log("Update iDRAC to 3.30.30.30 FAIL", FONT_RED)
	#		return False
			
	#	else:	
	#		os.system("reboot -f")
#===============================================================================
def Check_BP_VER():
	'''Check Backplane Version'''

	global BP_VER

	flag = False

	ret = Input_CMD_OS("racadm swinventory")
	if(ret == False):
		return False

	index = 0
	for i in range(len(ret)):
		if("FQDD" in ret[i] and "RAID.Backplane.Firmware.1" in ret[i]):
			Log("Index %d: %s"%(i, ret[i]), FONT_YELLOW)
			Log("Index %d: %s"%(i+2, ret[i+2]), FONT_YELLOW)
			index = i

	if(index == 0):
		Log("Check_BP_VER Fail (Couldn't find BP VER Index)", FONT_RED)
		return False

	if(BP_VER in ret[index + 2]):
		flag = True

	if(flag):
		Log("Check_BP_VER Pass", FONT_GREEN)
		return True
	else:
		Log("Check_BP_VER Fail", FONT_RED)
		return False
#===============================================================================
def Check_NIC_VER():
	'''Check NIC Version (BCM5720)'''

	global NIC_VER
		
	nic_list = ["NIC.Embedded.1-1-1", "NIC.Embedded.2-1-1"]
	
	for lom in nic_list:
		flag = False
		nic = ""
		ret = Input_CMD_OS("racadm hwinventory %s"%lom)
		if(ret == False):
			return False
		for i in ret:
			if("Family Version:" in i and NIC_VER in i):
				Log(i, FONT_YELLOW)
				nic = i.split(":")[1].strip()
				Log("NIC Version: %s"%(lom), FONT_YELLOW)
				flag = True
		if(flag):
			Log("Check_NIC_VER(%s) Pass"%lom, FONT_GREEN)
			continue
		else:
			Log("Check_NIC_VER(%s) Fail"%lom, FONT_RED)
			break
	if(flag):
		Log("Check_NIC_VER Pass", FONT_GREEN)
		return True
	else:
		Log("Check_NIC_VER Fail", FONT_RED)
		return False
#===============================================================================
def Check_PSU_VER():
	'''Check PSU Version'''

	global PSU_VER
	
	the_same_flag = False
	
	psu_list = ["PSU.Slot.1", "PSU.Slot.2"]

	ret = Input_CMD_OS("racadm swinventory")
	if(ret == False):
		return False
	for psu in psu_list:
		flag = False
		index = 0
		for i in range(len(ret)):
			if("FQDD" in ret[i] and "%s"%psu in ret[i]):
				Log("Index %d: %s"%(i, ret[i]), FONT_YELLOW)
				Log("Index %d: %s"%(i+2, ret[i+2]), FONT_YELLOW)
				index = i
			if(ret[10] == ret[18]):
				the_same_flag = True
		if(index == 0):
			Log("Check_PSU_VER Fail (Couldn't find %s VER Index)"%psu, FONT_RED)
			break
		else:
			if(PSU_VER in ret[index + 2] or NCNFF in ret[index + 2]):
				flag = True
				Log("Check_PSU_VER %s Pass"%psu, FONT_GREEN)			
				continue

	if(flag and the_same_flag):
		Log("Check_PSU_VER Pass", FONT_GREEN)
		return True
	else:
		if(flag == False):	
			Log("Check_PSU_VER Fail", FONT_RED)
		if(the_same_flag == False):
			Log("Check The Same PSU Fail", FONT_RED)
		return False
#===============================================================================
def Check_EXP_VER():
	'''Check SAS Expander FW Version'''

	flag = False

	ret = Input_CMD_OS("/opt/MegaRAID/perccli/perccli64 /c0/eall show all")
	if(ret == False):
		return False

	for i in ret:
		if(EXP_VER in i):
			Log(i, FONT_YELLOW)
			flag = True

	if(flag):
		Log("Check_EXP_VER Pass", FONT_GREEN)
		return True
	else:
		Log("Check_EXP_VER Fail", FONT_GREEN)
		return True
#===================================================================
def main():
	global VER
	global DEBUG_MODE
	global FAIL_CONTINUE
	global LOG_DIR
	global LOG_FILE

	INIT()

	Banner("SitKaII MB FW FVS Tool, By Foxconn Luciano Lu, Version: %s"%(VER))

	if(DEBUG_MODE):
		Log("DEBUG_MODE", FONT_WHITE)
	if(FAIL_CONTINUE):
		Log("FAIL_CONTINUE", FONT_WHITE)

	Log("Log Directory: %s"%(LOG_DIR), FONT_WHITE)
	Log("Log File: %s"%(LOG_FILE), FONT_WHITE)

	test_sequence = [
		Check_BIOS_VER,
		Check_CPLD_VER,
		Check_iDRAC_VER,
		# Check_PERC_VER,
		Check_NIC_VER,
		# Check_EXP_VER,
		Check_BP_VER,
		Check_PSU_VER
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
