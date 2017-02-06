#!/usr/bin/env python

from FileTransfer import FtpFileTransfer
from pathlib import Path
import os
import tarfile


class _main_():
	def fetchData():
		p_c = Path('credentials.txt').resolve()
		ftp = FtpFileTransfer(str(p_c))
		ftp.connect()
		p_s = Path('smina').resolve()
		if(os.path.exists(str(p_s)) == False):
			os.mkdir(str(p_s))
			os.chdir(str(p_s))
		else:
			os.chdir(str(p_s))
		ftp_files = ftp.list_files('challengedata')
		for x in (ftp_files):
			if(os.path.isfile(x) == False):
				ftp.download_file('challengedata/'+ x, str(p_s) + '/' + x)
		print("All the files have been downloaded to " + str(p_s))
		ftp.disconnect()
		
	
	fetchData()


