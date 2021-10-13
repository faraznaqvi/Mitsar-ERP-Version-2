#module loading 
import eventlet
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit, send
from baseline import data_acq
from flask import request
from pylsl import StreamInlet, resolve_stream
from scipy import signal
import numpy as np
import pandas as pd
from threading import Thread
import os 
import random


#module loading
app = Flask(__name__)

#configuration


app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
socketio = SocketIO(app)



#configuration



#global variables
timelist = [];
action = [];
global final_data
final_data_outside = [];
image_change_time_list = []
action_change_time_list = []
action_changed_index = 21
image_changed_index = 20
df = pd.DataFrame();
t = "./static/images/Hands"
files = os.listdir(t)
#images = random.sample(files, 40)


#assigning the app name
if __name__ == "__main__":
	socketio.run(app)
	Thread(target = func1).start()
	Thread(target = func2).start()


def func1(name,time_period):
	t = data_acq(name,time_period)
	return '1'
	



def func2():
	streams = resolve_stream('type', 'EEG')
    # create a new inlet to read from the stream
	inlet = StreamInlet(streams[0])
	sample, timestamp = inlet.pull_sample()
	temp = time.time()
	timelist.append(timestamp)

#assigning the app name

#defining the routes 
@app.route("/")
def hello():
	return render_template('index.html')


##### Socket code
@socketio.on('message')
def handle_message(message):
	if(message[0] == 'start'):
		#print(message[])
		file_name = message[1]+'-'+message[2]+'-'+message[3]
		func2()
		action.append("start")
		print("started")
		images = random.sample(files, 40)
		#print(images)
		func1(file_name,int(message[4])*60)
		#socketio.emit(images)
		return images
		

	if(message[0] == "stop"):
		file_name = message[1]+'-'+message[2]+'-'+message[3]
		func2()
		action.append("stop")
		data = {'Action':action,'Time':timelist}
		data = pd.DataFrame((data))
		data.to_csv('erp.csv')
		read_data = os.path.join(app.instance_path, file_name)+'.csv'
		print(read_data)
		read_data_to_csv = pd.read_csv(read_data)
		data_combining(read_data_to_csv,data,file_name)
		return "1"

	if(message == "left"):
		func2()
		#print("left")
		action.append("left")
		
	
	if(message == "right"):
		func2()
		#print("right")
		action.append("right")
			

	if(message == "image_changed"):
		func2()
		action.append("Image_Change")
		
	

def add_action_label(all_time,data,final_data):
	action_change_time_list = []
	for i in range(0,len(final_data.iloc[:,1])):
		action_change_time_list.append(data.Time[all_time]-final_data.iloc[i,1])
	temp = action_change_time_list.index(min(map(abs,action_change_time_list[0:len(action_change_time_list)])))
	return temp

def add_image_change_label(all_time,data,final_data):
	image_change_time_list = []
	for i in range(0,len(final_data.iloc[:,1])):	
		image_change_time_list.append(data.Time[all_time]-final_data.iloc[i,1])
	temp = image_change_time_list.index(min(map(abs,image_change_time_list[0:len(image_change_time_list)])))
	#final_data.iloc[temp,image_changed_index] = 1 
	return temp

def data_combining(read_data_to_csv,read_erp_data_to_csv,file_name):
	for all_time in range(0,len(read_erp_data_to_csv)):
		if(read_erp_data_to_csv.Action[all_time] == 'Image_Change'):
			print('Image Changing Index')
			index = add_image_change_label(all_time,read_erp_data_to_csv,read_data_to_csv)
			read_data_to_csv.iloc[index,20] = 1 
		if(read_erp_data_to_csv.Action[all_time] == 'left' or read_erp_data_to_csv.Action[all_time] == 'right'):
			print('Action Changing Index')
			index = add_action_label(all_time,read_erp_data_to_csv,read_data_to_csv)
			if(read_erp_data_to_csv.Action[all_time] == 'left'):
				read_data_to_csv.iloc[index,21] = 1
			else:
				if(read_erp_data_to_csv.Action[all_time] == 'right'):
					read_data_to_csv.iloc[index,21] = 2
	read_data_to_csv.to_csv(file_name+'.csv')