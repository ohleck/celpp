from FileTransfer import FtpFileTransfer
import os
import shutil
import prody

import plotly as py
import pandas as pd
import numpy as np
import seaborn as sns

import plotly.plotly as py
import plotly.tools as plotly_tools
import plotly.graph_objs as go
import plotly.offline as offline

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
%matplotlib inline

from scipy.stats import gaussian_kde

from IPython.display import HTML

py.sign_in("juz19", "gns0PM7FQ368i6A8tNOZ")


def fetch_visual_file():
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

	if(os.path.isdir(wd + '/challengedata_Visualizaiton')==False):#creates challengedata folder if it doesn't exist			
    	print('challengedata_Visualizaiton directory does not exists. ')
    	os.mkdir(wd + '/challengedata_Visualizaiton')
    	os.chdir(wd + '/challengedata_Visualizaiton')
	else: #changes to challengedata folder if it exists
		os.chdir(wd + '/challengedata_Visualizaiton')
			
	ftp = FtpFileTransfer(cred)
	print('Connecting to ftp.box.com')
	ftp.connect() 
	print('Connected to ftp')
		
	ftp_files = ftp.list_files('challengedata')#creates list of files from box
	for x in (ftp_files): 
    	if (x == 'visual.txt'):
        	ftp.download_file('challengedata/' + x, wd + '/challengedata/' + x)

	ftp.disconnect()
	print('Disconnected from ftp')


def box_plot(rmsd, week_num):
    x_data = list(rmsd.keys())
    y_data = []
    for x in x_data:
        data = rmsd.get(x)
        y_data.append(data)
    N = len(x_data)
    colors = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

    traces = []

    for xd, yd, cls in zip(x_data, y_data, colors):
        traces.append(go.Box(
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker=dict(size=2,),
                line=dict(width=1),))

        layout = go.Layout(title='RMSD for all Targets in Week' + str(week_num),
                           yaxis=dict(autorange=True,showgrid=True,zeroline=True,dtick=5,
                                      gridcolor='rgb(255, 255, 255)', gridwidth=1,
                                      zerolinecolor='rgb(255, 255, 255)',zerolinewidth=2,),
                           margin=dict(l=40,r=30,b=80,t=100,),
                           paper_bgcolor='rgb(243, 243, 243)',
                           plot_bgcolor='rgb(243, 243, 243)',
                           showlegend=False)

    fig = go.Figure(data=traces, layout=layout)
    
    return fig


def bar_plot(rmsd, week_num):
    x_data = list(rmsd.keys())
    y_data = []
    for x in x_data:
        data = rmsd.get(x)
        y_data.append(data)
    y_best_rmsd = []
    y_first_rmsd = []
    for y in y_data:
        min_rmsd = min(y)
        first_rmsd = y[0]
        y_best_rmsd.append(min_rmsd)
        y_first_rmsd.append(first_rmsd)
    trace1 = go.Bar(
        x = x_data,
        y = y_best_rmsd,
        name='Best RMSD'
    )

    trace2 = go.Bar(
        x = x_data,
        y = y_first_rmsd,
        name='First Pose RMSD'
    )

    data = [trace1, trace2]
    layout = go.Layout(title='Best and First Pose RMSD for all Targets in Week' + str(week_num),
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    
    return fig
    

