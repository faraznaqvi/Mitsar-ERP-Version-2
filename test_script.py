# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:36:54 2021

@author: Neurocomputation Lab
"""

import pandas as pd
#from baseline import data_acq
#from pylsl import StreamInlet, resolve_stream
image_change_time_list = []
action_change_time_list = []
erp = pd.read_csv ('D:/Mitsar-ERP-Version-2/erp.csv')

read_data = pd.read_csv ('D:/Mitsar-ERP-Version-2/faraz.csv')

action_changed_index = 21
image_changed_index = 20
action = 4

actions = [0]* len(erp.iloc[:,1])
image_change_time = [0]* len(erp.iloc[:,1])


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
	final_data.iloc[temp,image_changed_index] = 1 
	return temp

def data_combining(read_data_to_csv,read_erp_data_to_csv):
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
	read_data_to_csv.to_csv("test.csv")

data_combining(read_data,erp)

#final_data = data_acq("faraz",2)

# divide erp list into two list one having only action time and other having image change time
# this will help to traverse and put label on two different dataframe positions for action and image change

# for j in range(0,len(erp.Time)):
#     for i in range(0,len(data.iloc[:,1])):
#         image_change_time_list.append(erp.Time[action]-data.iloc[i,1])
#     temp = image_change_time_list.index(min(map(abs,image_change_time_list[0:len(image_change_time_list)])))
#     data.iloc[temp,21] = 1
    

# for j in range(0,len(erp.Time)):
#     for i in range(0,len(data.iloc[:,1])):
#         action_change_time_list.append(erp.Time[action]-data.iloc[i,1])
#     temp = action_change_time_list.index(min(map(abs,action_change_time_list[0:len(action_change_time_list)])))
#     data.iloc[temp,21] = 1




