import os

import plotly as py
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.tools as plotly_tools
import plotly.graph_objs as go
import plotly.offline as offline

import matplotlib.pyplot as plt
import matplotlib as mpl

def readJson(cur_dir):
	rmsd = {}
	week_num = ''
	protocol = ''
	for sub in os.listdir(cur_dir):
		if sub.endswith('.txt') or sub.endswith('.tsv'):
			continue
		li = []
		target = cur_dir + '/' + sub
		if not week_num:
			try:
				with open(target + '/visual.txt', 'r') as visual:
					line = visual.next().split()
					week_num = line[0]
					protocol = line[1]
			except IOError as e:
				print(e)
				continue
		try:
			with open(target + '/rmsd.txt', 'r') as data:
				for s in data.readlines():
					li.append(float(s[7:]))
		except IOError as e:
				print(e)
				continue
		rmsd[sub] = li
	return rmsd, week_num, protocol

def box_plot(rmsd, week_num):
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
    N = len(x_data)
    colors = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

    traces = []

    for xd, yd, ybest, yfirst, cls in zip(x_data, y_data, y_best_rmsd, y_first_rmsd, colors):
        traces.append(go.Box( 
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=1,
                whiskerwidth=1,
                pointpos = -2,
                fillcolor=cls,
                marker=dict(size=3,),
                line=dict(width=1.5),))
        
        traces.append(go.Scatter(
            showlegend = False, 
            legendgroup = 'Best RMSD', 
            y = ybest, 
            x = xd, 
            name = xd + ' Best RMSD', 
            fillcolor=cls,
            marker = dict(size = 15, symbol = 'square-open', ), ))
        
        traces.append(go.Scatter(
            showlegend = False, 
            legendgroup = 'First Pose RMSD', 
            y = yfirst, 
            x = xd, 
            name = xd + ' First Pose RMSD', 
            fillcolor = cls, 
            marker = dict(size = 15, symbol = 'star', ),))

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

def bar_plot(averages, week_num):
    x_data = list(averages.keys())
    trace1 = go.Bar(
        x = x_data,
        y = [x[0] for x in averages.values() if x],
        name='Best RMSD'
    )

    trace2 = go.Bar(
        x = x_data,
        y = [x[1] for x in averages.values() if x],
        name='First Pose RMSD'
    )

    data = [trace1, trace2]
    layout = go.Layout(title='Best and First Pose RMSD for all Targets in Week' + str(week_num),
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    
    return fig
	
def generate_reports():
	py.sign_in("juz19", "gns0PM7FQ368i6A8tNOZ")
	try:
		if not os.path.exists('challengedata'):
			os.makedirs('challengedata')
	except IOError as e:
		print('Failed to create directory: challengedata. '+e)
		return
	averages = {}
	url_by_week = {}
	for sub in os.listdir(os.getcwd()+'/challengedata'):
		if sub.startswith('celpp_week'):
			rmsd, week_num, protocol = readJson(sub)
			print(week_num)
			if not rmsd:
				continue
			averages[week_num] = stats(rmsd)
			url_by_week[week_num] = py.plot(box_plot(rmsd, week_num), filename='Box Plot - '+week_num.split('_')[1][4:], auto_open=False)
			html_string = '''
			<html>
				<head>
					<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
					<style>body{ margin:0 100; background:whitesmoke; }</style>
				</head>
				<body>
					<h1>Week '''+week_num.split('_')[1][4:]+''' Visualization of RMSD for Smina</h1>

					<!-- *** Section 1 *** --->
					<h2>Section 1: RMSDs for All Targets in Week '''+week_num.split('_')[1][4:]+'''</h2>
					<iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
			src="''' + url_by_week[week_num] + '''.embed?width=800&height=550"></iframe>
					
				</body>
			</html>'''
			
			try:
				if not os.path.exists('visual'):
					os.makedirs('visual')
				if not os.path.exists('visual/'+week_num):
					os.makedirs('visual/'+week_num)
				
				f = open('visual/'+week_num+'/report.html','w')
				f.write(html_string)
				f.close()
			except IOError as e:
				print('Failed to create report.html. '+e)
				break
	generate_summary(averages, week_num, url_by_week)

def generate_summary(averages, week_num, url_by_week):
	summary_url = py.plot(bar_plot(averages, week_num) ,filename='Best and First Plot', auto_open=False)
	
	buttons = ''''''
	for week, url in url_by_week.items():
		buttons += '''<button onclick='location.href="'''+ url +'''"'>'''+week.split('_')[1][4:]+'''</button>'''
	html_string = '''
	<html>
		<head>
			<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
			<style>body{ margin:0 100; background:whitesmoke; }</style>
		</head>
		<body>
			<h1>Visualization Summary of RMSD for Smina</h1>
			<iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
	src="''' + summary_url + '''.embed?width=800&height=550"></iframe><br>
			'''+buttons+'''
		</body>
	</html>'''
	
	try:
		f = open('summary_report.html','w')
		f.write(html_string)
		f.close()
	except IOError as e:
		print('Failed to create summary_report.html. '+e)
	
def stats(rmsd):
	li = [x for x in rmsd.values() if np.inf not in x]
	if not li:
		return []
	ave_first = sum([x[0] for x in li])/len(li)
	ave_best = sum([min(x) for x in li])/len(li)
	return [round(ave_best, 6), round(ave_first, 6)]
	
generate_reports()