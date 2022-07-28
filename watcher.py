# Python program to explain os.scandir() method

# importing os module
import os
import subprocess
import filecmp
import time
import shutil

def listPorts():
	# Directory to be scanned
	dir_path = r'/dev'
	notify_string = ""
	# list to store files
	res = []

	for (dir_path, dir_names, file_names) in os.walk(dir_path):
	    res.extend(file_names)

	for i in res:
		if "tty." in i:
			#print(i)
			notify_string = notify_string.join(i)
	
	return(res)

def notify(title, text):
	CMD = '''
	on run argv
	  display notification (item 2 of argv) with title (item 1 of argv)
	end run
	'''
	subprocess.call(['osascript', '-e', CMD, title, text])

def check_unique(inList):
	outString = ""
	for x in inList:
		if inList.count(x) < 2:
			#print(x)
			outString = outString + x
	return outString

if __name__ == "__main__":
    while True:
	    notify_string = ""
	    notify_title = "Serial Port Change"
	    # Get Current Ports
	    with open(r'current_ports.txt', 'w') as cfp:
	    	results = listPorts()
	    	for port in results:
	    		if "tty." in port:
	    			cfp.write("%s\n" % port)
	    	cfp.close()
	    	port_list = []
	    	current_port = open(r'current_ports.txt', 'r')
	    	old_ports =  open(r'old_ports.txt', 'r')
	    	for linex in old_ports:
	    		port_list.append(linex)
	    	for line in current_port:
	    		port_list.append(line)
	    	notify_string = check_unique(port_list)
	    	time.sleep(3)
	    if len(notify_string) > 1:
	    	notify(notify_title, notify_string)
	    	shutil.copyfile('current_ports.txt', 'old_ports.txt')
    	



