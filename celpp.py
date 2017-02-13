#!/usr/bin/env python

from FileTransfer import FtpFileTransfer
import os
import subprocess
import shlex


class _main_():
	
	
	def fetchData():
		if os.path.isdir(os.path.expanduser("~/Desktop/celpp")) == False:
			os.mkdir(os.path.expanduser("~/Desktop/celpp"))
		else: 
			print("All Files will go into the celpp folder")
			
		cred = os.path.expanduser("~/Desktop/celpp/credentials.txt")
		try: 
			print("Trying to open credentials.txt")
			fo = open(cred, 'r')
			fo.close()
		except: 
			print("Writing credentials.txt file")
			fo = open(cred, 'w')
			fo.write("host ftp.box.com\nuser nlr23@pitt.edu\npass h@il2pitt1\npath\ncontestantid 33824\nchallengepath /challengedata\nsubmissionpath /33824")
			fo.close()
		
		ftp = FtpFileTransfer(cred)
		print("Connecting to ftp.box.com")
		ftp.connect()
		print("Connected to ftp")
		
		if(os.path.isdir(os.path.expanduser("~/Desktop/celpp/challengedata"))==False):
			os.mkdir(os.path.expanduser("~/Desktop/celpp/challengedata"))
			os.chdir(os.path.expanduser("~/Desktop/celpp/challengedata"))
		else:
			os.chdir(os.path.expanduser("~/Desktop/celpp/challengedata"))
		ftp_files = ftp.list_files('challengedata')
		count = 0 
		for x in (ftp_files):
			split = os.path.splitext(x)
			dir = os.path.splitext(split[0])
			if(str(split[1]) == 'gz'):
				if os.path.isfile(x) == True:
					print('Unzipping folder ' + str(dir))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
				elif os.path.isdir(str(dir[0])) == True:
					pass
					print(str(dir[0]) + ' exists')
				else: 
					ftp.download_file('challengedata/'+ x,  os.path.expanduser("~/Desktop/celpp/challengedata") + '/' + x)
					print('Unzipping folder ' + str(dir))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
					count = count + 1
					print(str(dir[0]) + " was just added to the challengedata folder")
			else: 
				pass
		print("challengedata has been updated. " + str(count) + " week(s) was/were just added.")		
		print("Disconnecting from ftp")
		ftp.disconnect()
	
	fetchData()


