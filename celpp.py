#!/usr/bin/env python

from FileTransfer import FtpFileTransfer
import os
import subprocess
import shlex


class _main_():
	
	
	def fetchData():
		if os.path.isdir(os.path.expanduser("~/Desktop/celpp")) == False: #creates celpp folder on users desktop if not already there
			os.mkdir(os.path.expanduser("~/Desktop/celpp"))
		else: 
			print("All Files will go into the celpp folder")
			
		cred = os.path.expanduser("~/Desktop/celpp/credentials.txt")
		try: #attempts to connect to file required to connect to ftp
			print("Trying to open credentials.txt")
			fo = open(cred, 'r')
			fo.close()
		except: #writes file required to connect to ftp if not already made
			print("Writing credentials.txt file")
			fo = open(cred, 'w')
			fo.write("host ftp.box.com\nuser nlr23@pitt.edu\npass h@il2pitt1\npath\ncontestantid 33824\nchallengepath /challengedata\nsubmissionpath /33824")
			fo.close()
		
		if(os.path.isdir(os.path.expanduser("~/Desktop/celpp/challengedata"))==False):#creates challengedata folder if it doesn't exist
			os.mkdir(os.path.expanduser("~/Desktop/celpp/challengedata"))
			os.chdir(os.path.expanduser("~/Desktop/celpp/challengedata"))
		else: #changes to challengedata folder if it exists
			os.chdir(os.path.expanduser("~/Desktop/celpp/challengedata"))
			
			
		ftp = FtpFileTransfer(cred)
		print("Connecting to ftp.box.com")
		ftp.connect() 
		print("Connected to ftp")
		
		ftp_files = ftp.list_files('challengedata')#creates list of files from box
		count = 0 #keep track number of files added to local folder
		for x in (ftp_files):
			split = os.path.splitext(x)
			dir = os.path.splitext(split[0])
			if(str(split[1]) == '.gz'):
				if os.path.isfile(x) == True:#if it finds the zip file in local folder, unzips and deletes zippped file
					print('Unzipping folder ' + str(dir[0]))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
				elif os.path.isdir(str(dir[0])) == True:#if it finds the unzipped directory in local folders
					print(str(dir[0]) + ' exists')
				else: #if it can't find the week in any format; downloads, unzips, and removes zipped file
					ftp.download_file('challengedata/'+ x,  os.path.expanduser("~/Desktop/celpp/challengedata") + '/' + x)
					print('Unzipping folder ' + str(dir[0]))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
					count = count + 1
					print(str(dir[0]) + " was just added to the challengedata folder")
			else: 
				ftp.download_file('challengedata/'+ x,  os.path.expanduser("~/Desktop/celpp/challengedata") + '/' + x)
		print("challengedata has been updated. " + str(count) + " week(s) was/were just added.")		
		print("Disconnecting from ftp")
		ftp.disconnect()
	
	fetchData()


