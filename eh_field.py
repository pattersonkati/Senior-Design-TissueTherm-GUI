import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import math


def eh_plot(file, ch1, ch2, ch3, ch4, fig_opt):
    data = pd.read_csv(file, skiprows=16)
    e1 = None
    e2 = None
    h1 = None 
    h2 = None
    global fig
    fig = plt.figure(figsize=(6, 3))
    time = data.iloc[::10,0].astype(float)
    time = time.iloc[10:]
    channels = np.array([ch1, ch2, ch3, ch4])
    
    #orient data variables based on user interface options
    if ch1 == 1:
        e1 = np.array(data.iloc[::10, 1].astype(float))
    elif ch1 == 2:
        h1 = np.array(data.iloc[::10, 1].astype(float))

    if ch2 == 1:
        if e1 is not None:
            e2 = np.array(data.iloc[::10, 2].astype(float))
        else:
            e1 = np.array(data.iloc[::10, 2].astype(float))
    elif ch2 == 2:
        if h1 is not None:
            h2 = np.array(data.iloc[::10, 2].astype(float))
        else:
            h1 = np.array(data.iloc[::10, 2].astype(float))
    if ch3 == 1:
        if e1 is not None:
            e2 = np.array(data.iloc[::10, 3].astype(float))
        else:
            e1 = np.array(data.iloc[::10, 3].astype(float))
    elif ch3 == 2:
        if h1 is not None:
            h2 = np.array(data.iloc[::10, 3].astype(float))
        else:
            h1 = np.array(data.iloc[::10, 3].astype(float))

    if ch4 == 1:
        if e1 is not None:
            e2 = np.array(data.iloc[::10, 4].astype(float))
        else:
            e1 = np.array(data.iloc[::10, 4].astype(float))
    elif ch4 == 2:
        if h1 is not None:
            h2 = np.array(data.iloc[::10, 4].astype(float))
        else:
            h1 = np.array(data.iloc[::10, 4].astype(float))
    
    #Calculate strength values

    #convert Vpp to dBm
    if e1 is not None:
        e1 = e1[10:]
        e1 = e1 * 1000 #convert to mVpp
        e1 = 10 * np.log10((e1/2.828) ** 2 / (50*1000)) # convert mVpp to dBm
        e1 = 10 ** ((e1 + 113.2 - 20*np.log10(27.12))/20) # convert dBm to V/m
    if e2 is not None:
        e2 = e2[10:]
        e2 = e2 * 1000 #convert to mVpp
        e2 = 10 * np.log10((e2/2.828) ** 2 / (50*1000))
        e2 = 10 ** ((e2 + 113.2 - 20*np.log10(27.12))/20) # convert dBm to V/m
    if h1 is not None:
        h1 = h1[10:]
        h1 = h1 * 1000 #convert to mApp
        h1 = 10 * np.log10((h1/2.828) ** 2 / (50*1000)) #convert mApp to dBm
        h1 = 10 ** (((h1 - 85.1 - 20*np.log10(27.12))/20) / 4*math.pi * 0.0000001)
    if h2 is not None:
        h2 = h2[10:]
        h2 = h2 * 1000 #convert to mApp
        h2 = 10 * np.log10((h2/2.828) ** 2 / (50*1000)) #convert mApp to dBm
        h2 = 10 ** (((h2 - 65.2 - 20*np.log10(27.12))/20) / (4*math.pi * 0.0000001))


    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")

    if np.count_nonzero(channels == 1) == 2 and fig_opt == 1:
        if 'fig' not in globals():
            fig = plt.figure(figsize=(6, 3))
            ax = fig.add_subplot(111)  
        else:
            plt.close(fig)
            fig = plt.figure(figsize=(6, 3))
            ax = fig.add_subplot(111)   

        e_diff = np.abs(e1 - e2)
        ax.plot(time, e_diff, label = 'Electric Field (V/m)')
        ax.set_title("Electric Field Strength vs Time")
        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.85, top=0.85)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Field Strength (V/m)')

        file_e = f"e-Strength_{timestamp}.png"
        fig.savefig(file_e)

    if np.count_nonzero(channels == 2) == 2 and fig_opt == 2:
        if 'fig' not in globals():
            fig = plt.figure(figsize=(6, 3))
            ax = fig.add_subplot(111)  
        else:
            plt.close(fig)
            fig = plt.figure(figsize=(6, 3))
            ax = fig.add_subplot(111)  
         

        h_diff = np.abs(h1 - h2)
        ax.plot(time, h_diff, label = 'Magnetic Field (A/m)')
        ax.set_title("Magnetic Field Strength vs Time")
        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.85, top=0.85)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Field Strength (A/m)', labelpad=20)

        file_h = f"h-Strength_{timestamp}.png"
        fig.savefig(file_h)

    return fig