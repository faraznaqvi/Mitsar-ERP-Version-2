from pylsl import StreamInlet, resolve_stream
from scipy import signal
import numpy as np
import pandas as pd
import time
from datetime import datetime
import os 
import random

def data_acq(name, time_Duration):
    
    image_time = []
    action = []
    time_stamp = []
    total_samples = []
    
    check = True
    ##name = input("Enter your name : ")
    ##time_Duration = int(input("Enter time in seconds : "))
    file_name ="./instance/" + name + ".csv"
    t = "./static/images/Hands"
    files = os.listdir(t)
    images = random.sample(files, 40)
    
    try:
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')
        # create a new inlet to read from the stream
        inlet = StreamInlet(streams[0])
        t1 = time.time()
        while check:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
            t2 = time.time()
            sample, timestamp = inlet.pull_sample()
            time_stamp.append(timestamp)
            #temp = time.time()
            #total_samples.append(temp)
            total_samples.append(sample) 
            print(t2-t1)
            if (t2-t1 >= time_Duration):
                check = False
        time_df = pd.DataFrame((time_stamp))
        sample_df = pd.DataFrame((total_samples))
        time_image = [0]*len(time_df)
        action = [0]*len(time_df)
        data = pd.DataFrame(({'Image Change Time': time_image, 'Action':action}))
        Data_df = pd.concat((time_df,sample_df,data), axis =1)
        Data_df.to_csv(file_name)
        print(file_name)
        
        return Data_df
        
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e