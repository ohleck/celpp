#!/usr/bin/env python

from FileTransfer import FtpFileTransfer
import os
import shutil
import prody



class _main_():
	

	
	
	
	def fetchData():
		
		global wd
		wd = str(os.getcwd()) 
		
		print('All Files will go into the celpp folder')
			
		cred = (wd + '/credentials.txt')
		try: #attempts to connect to file required to connect to ftp
			print('Trying to open credentials.txt')
			fo = open(cred, 'r')
			fo.close()
		except: #writes file required to connect to ftp if not already made
			print('Writing credentials.txt file')
			fo = open(cred, 'w')
			fo.write('host ftp.box.com\nuser nlr23@pitt.edu\npass #hail2pitt1\npath\ncontestantid 33824\nchallengepath /challengedata\nsubmissionpath /33824')
			fo.close()
		
		if(os.path.isdir(wd + '/challengedata')==False):#creates challengedata folder if it doesn't exist
			os.mkdir(wd + '/challengedata')
			os.chdir(wd + '/challengedata')
		else: #changes to challengedata folder if it exists
			os.chdir(wd + '/challengedata')
			
			
		ftp = FtpFileTransfer(cred)
		print('Connecting to ftp.box.com')
		ftp.connect() 
		print('Connected to ftp')
		
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
					pass
				else: #if it can't find the week in any format; downloads, unzips, and removes zipped file
					ftp.download_file('challengedata/'+ x,  wd + '/challengedata/' + x)
					print('Unzipping folder ' + str(dir[0]))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
					count = count + 1
					print(str(dir[0]) + ' was just added to the challengedata folder')
			else:
				ftp.download_file('challengedata/'+ x,  wd + '/challengedata/' + x)
		print('challengedata has been updated. ' + str(count) + ' week(s) was/were just added.')		
		print('Disconnecting from ftp')
		ftp.disconnect()
	
	def	align():
		
		global wd 
		ans = wd +'/challengedata/answers'
		if os.path.isdir(ans)==False: #if the answers directory isnt formed make it
			os.mkdir(wd+'/challengedata/answers')
		rddir = wd+'/challengedata/rdkit-scripts'
		if os.path.isdir(rddir)==False:
			a='git clone https://github.com/dkoes/rdkit-scripts'
			os.system(a)
		data = os.listdir(wd+'/challengedata')
		for x in (data):#for each weeks data
			if x=="readme.txt" or x=="latest.txt" or x=="answers" or x=="rdkit-scripts" or x=='PDBfiles' or x=='visual.txt': 
				pass
			else:
				toDir = wd +'/challengedata/answers/' + x
				if os.path.isdir(toDir)==False: #if the path to answers dir doesnt exist 
					os.mkdir(toDir) #make directory		
				dock=os.listdir(wd+'/challengedata/'+x)
				for y in (dock):
					a = str(os.getcwd()+'/answers/'+x+'/'+y+'/lmcss_docked.sdf')
					if y=='readme.txt' or y=='new_release_structure_sequence_canonical.tsv' or y == 'new_release_structure_nonpolymer.tsv' or y=='new_release_crystallization_pH.tsv' or y=='new_release_structure_sequence.tsv':
						pass
					elif(os.path.isfile(a)==True):
						pass
					else:
						input = os.listdir(wd+'/challengedata/'+x+'/'+y)
						for z in (input):
							if z.startswith("LMCSS") and z.endswith(".pdb"):
								if(z.endswith("lig.pdb")):
									pass
								else:
									sts = str("grep ATOM "+ z+" > lmcss_rec.pdb")#creates receptor .pdb file
									cd = wd+'/challengedata'
									os.chdir(cd+'/'+x+'/'+y)#change directory to week/ligand
									os.system(sts)#runs and creates receptor .pbd file
									os.chdir(cd)#back to challenge directory
									input = os.listdir(cd+'/'+x+'/'+y)#lists files inside ligand in certain week
									for z in (input):
										if z.endswith(".smi"):# changes .smi -> lig.sdf
											cd = str(os.getcwd())
											sts = str(" "+cd+'/'+x+'/'+y+'/'+z +" lig.sdf --maxconfs 1")
											os.chdir(cd+'/'+x+'/'+y)
											os.system(cd+'/rdkit-scripts/rdconf.py'+ sts)
											os.chdir(cd)
											
									for z in (input): # runs smina
										if z.endswith("lig.pdb"):
											sts=str("smina -r lmcss_rec.pdb -l lig.sdf --autobox_ligand "+z+" -o lmcss_docked.sdf")
											cd=str(os.getcwd())#lignad directory
											os.chdir(cd+'/'+x+'/'+y)
											os.system(sts)
											os.chdir(cd)
											
									cur = str(os.getcwd()+'/answers/'+x+'/'+y)
									if (os.path.isdir(cur)==True):
										os.chdir(cd+'/'+x+'/'+y)
										os.getcwd()##
										input = os.listdir(cd+'/'+x+'/'+y)
										print(input)##
										for i in (input):
											if i.endswith("lig.pdb"): 
												#see if pdb exists
												protein = prody.fetchPDB(y)
												#NEED NUMPY ARRAY 
												prody.writeArray('lmcss_docked_array.sdf', array)
												prody.superpose('lmcss_docked.sdf', protein, weights=None)											
												sts=str("obrms -f "+i+" lmcss_docked.sdf")
												#run obrms
												# parse results and output to the visualization txt file
												os.system(sts)
												os.chdir(wd+'/challengedata/')
												f=open('visual.txt', 'ab+')
												f.write(x+'	smina	'+y+'\n')
												f.close
												curdir = str(cd+'/'+x+'/'+y+'/lmcss_docked.sdf')
												todir = str(cd+'/answers/'+x+'/'+y+'/')
												shutil.copy(curdir, todir)
												print(curdir)
												break
										os.chdir(wd)
									else:
										os.mkdir(cur)
										os.chdir(cd+'/'+x+'/'+y)
										input = os.listdir(cd+'/'+x+'/'+y)
										for i in (input):
											if i.endswith("lig.pdb"):
												protein = prody.fetchPDB(y)
												prody.writeArray('lmcss_docked_array.sdf', array)
												prody.superpose('lmcss_docked.sdf', protein, weights=None)											

												sts=str("obrms -f "+i+" lmcss_docked.sdf")
												os.system(sts)
												os.chdir(wd+'/challengedata/')
												f=open('visual.txt', 'ab+')
												f.write(x+'	smina	'+y+'\n')
												f.close
												curdir = str(cd+'/'+x+'/'+y+'/lmcss_docked.sdf')
												todir = str(cd+'/answers/'+x+'/'+y+'/')
												shutil.copy(curdir, todir)
												print(curdir)
												break
								os.chdir(wd)				
								
	def compare(): 
		
		###get PDB files from databank that are associated with each protein for later use
		##change directory
		
		#create a folder that contains all pdb files from the PDB if it does not exist
		prody.pathPDBFolder(wd + '/challengedata/PDBfiles')
			
		#list of proteins that need to be downloaded
		weeks = []
		for(_, dirnames, _) in os.walk(wd + '/challengedata'): 
			if (dirnames=='latest.txt' or dirnames=='answers' or dirnames =='rdkit-scripts'):
				pass
			elif (dirnames not in weeks): 
				weeks.extend(dirnames)
		proteins = [x for x in weeks if 'celpp' not in x]
		
		#download pdb using prody 
		for x in proteins:
			if x=='rdkit-scripts' or x=='PDBfiles' or x=='answers': 
				pass
			else:
				protein = prody.fetchPDB(x)
			#prody.superpose()		
			
		
		
	def uploadData():#uploads zip files containing docking predictions to contestant folder specified in credentials.txt
		print('Uploading files to box contestant folder')
		cred = wd + '/credentials.txt'
		ftp = FtpFileTransfer(cred)
		print('Connecting to ftp.box.com')
		ftp.connect() 
		print('Connected to ftp')
		ftp_files = ftp.list_files(ftp.get_contestant_id())#creates list of files from box
		d = []
		for(_, dirnames, _) in os.walk(wd + '/protocols'):
			d.extend(dirnames)
			break
		for dir in (d):#NOT A FAN OF THE NESTED FOR LOOPS, WILL TRY TO FIND BETTER WAY TO IMPLEMENT THIS
			for(_,_,filenames) in os.walk(wd + '/protocols/' + dir):
				f = []
				f.extend(filenames)
				print('Uploading files for ' + dir)
				for x in (f): 
					if((x in ftp_files) == False):
						file = wd + '/protocols/' + dir + '/' + x
						remote_dir = ftp.get_remote_submission_dir()
						remote_file_name = os.path.basename(file)
						ftp.upload_file_direct(file, remote_dir, remote_file_name)
					else:
						pass	
		print('All the files have been uploaded. Disconnecting from ftp')
		ftp.disconnect()
	
		

	fetchData()
	align()
	#uploadData()
