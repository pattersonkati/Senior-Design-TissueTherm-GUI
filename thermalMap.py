import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import datetime
'''
thermalMap.py
Author: Kati Patterson

Purpose: Generate a 3D thermal map that adjusts with the user-defined sample characteristics and updates its 
    scatterplot colors in real-time based on a provided .csv 
    **Format of .csv expected is in Users Manual


'''

#define probes locations
probe_x = [115, 115, 115, 115, 90, 90, 90, 90, 65, 65, 65, 65] 
probe_y = [52.5, 77.5, 102.5, 127.5, 52.5, 77.5, 102.5, 127.5, 52.5, 77.5, 102.5, 127.5] 
probe_z = [15, 20, 5, 10, 20, 5, 10, 15, 5, 10, 15, 20] 


# function to turn on/off probe labels
def update_labels(show_labels, scat):
    if show_labels:
        for i in range(len(probe_x)):
            scat.text(probe_x[i], probe_y[i], probe_z[i], str(i+1))
    else:
        for text in scat.texts:
            text.remove()
    return scat,

# function to produce the 3D thermal animation
def create_3d(shape, l, w, h, low, high, file):

     ## Create Ellipsoidal Surface (to represent sample) ##
    def animate():

        #creating figure
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111, projection='3d') # to specify 3d plot (plt.figure() defaults to 2d)

        # choose shape to plot based on user input
        if shape == "Circle/Ellipsoid":
            #radii corresponding to the coefficients:
            coefs = (l/2.0, w/2.0, h/2.0)
            rx, ry, rz = coefs

            #build cartesian coordinates for ellipsoid
            u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
            x = rx * np.cos(u)*np.sin(v) + 100
            y = ry * np.sin(u)*np.sin(v) + 100
            z = rz * np.cos(v) + h/2 - 10

            #build sample plot
            ax.plot_surface(x, y, z, alpha = 0.2, cmap = 'binary')

        elif shape == "Square/Rectangle":
            phi = np.arange(1,10,2)*np.pi/4
            Phi, Theta = np.meshgrid(phi, phi)

            x = np.cos(Phi)*np.sin(Theta) 
            y = np.sin(Phi)*np.sin(Theta) 
            z = np.cos(Theta)/np.sqrt(2) 
            a,b,c = l, w, h
            x = x*a + 100
            y = y*b + 100
            z = z*c + h/2
            ax.plot_surface(x,y,z, cmap='gray', alpha=0.2)


        #adding title, labels, axes
        #ax.set_title("3D Thermal Display", fontsize=16)
        ax.set_xlabel('X-axis (mm)')
        ax.set_xlim3d([0, 200])
        ax.set_ylabel('Y-axis (mm)')
        ax.set_ylim3d([0, 200])
        ax.set_zlabel('Z-Axis (mm)')
        ax.set_zlim3d([0, 100])

        #read data
        data= pd.read_csv(file)
        colors = data.iloc[0, 1:13].values


        #configure scatter plot
        scat = ax.scatter(probe_x, probe_y, probe_z, s = 150, c = colors, alpha = 0.8, cmap='YlOrRd', vmin=low, vmax=high)
        scat.set_cmap('YlOrRd')
        plt.colorbar(scat)

        # Function to update colors real-time
        def update_colors(i, scat):

            data = pd.read_csv(file)
            new_colors = data.iloc[i, 1:13].values
            props=dict(boxstyle='round', facecolor='white', alpha = 0.9)
            text_box = fig.text(0.2, 0.8, s="", fontsize=12, verticalalignment='top', bbox=props)
            
            #plot time box in top left 
            if i == len(data):
                text_box.remove()
            else:
                text_box.set_text("Time (s): " + str(data.iloc[i, 0]))
            
            
            scat.set_array(new_colors)
            return scat,
    
        ani = animation.FuncAnimation(fig, update_colors, frames=len(data), fargs=(scat,), interval=3000, repeat=False)
                    

        return ani, fig, ax
    
    anim, fig, ax = animate()

    return anim, fig, ax


    