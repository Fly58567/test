#===================================================================#
#       Tool Name: SitKaII Stress Tool                              #
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

global STRESS_DIR
STRESS_DIR = os.path.join(ROOT_DIR, "LinuxStress")

global DEBUG_MODE
DEBUG_MODE = True

global FAIL_CONTINUE
FAIL_CONTINUE = False

global TEST_TIME
TEST_TIME = 60

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
def Stress_Test():
	'''Run Stress Test'''

	flag = False

	os.chdir(STRESS_DIR)

	Input_CMD_OS("chmod 755 *")

	cmd = "./stress --cpu 10 --io 1 --vm 1 --vm-bytes 1G --hdd 1 --timeout %ds -v"%(TEST_TIME)
	ret = Input_CMD_OS_1(cmd)

	os.chdir(ROOT_DIR)

	for i in ret:
		if("successful run completed" in i):
			flag = True

	if(flag):
		Log("Stress_Test Pass", FONT_GREEN)
		return True
	else:
		Log("Stress_Test Fail", FONT_RED)
		return False
#===============================================================================
def main():
	global VER
	global DEBUG_MODE
	global FAIL_CONTINUE
	global LOG_DIR
	global LOG_FILE

	INIT()

	Banner("SitKaII Stress Tool, By Foxconn Luciano Lu, Version: %s"%(VER))

	if(DEBUG_MODE):
		Log("DEBUG_MODE", FONT_WHITE)
	if(FAIL_CONTINUE):
		Log("FAIL_CONTINUE", FONT_WHITE)

	Log("Log Directory: %s"%(LOG_DIR), FONT_WHITE)
	Log("Log File: %s"%(LOG_FILE), FONT_WHITE)

	test_sequence = [
		Stress_Test,
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
