#Imported Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np
import signal
from multiprocessing import Queue
import matplotlib.animation as animation
import datetime
import threading
import csv
#Imported Files
import thermalMap as tm
from readData import readData
from eh_field import eh_plot
import tempsTable as tt
import matplotlib.pyplot as plt

#Global Variables
show_labels = False
queue = Queue()
global fig1, scat
global anim1
global stop_flag
global temps_file
sec = 0

# # # # # # # # # # # # # # # # # # # # # # # 
# ---------- Create Overall Frame ---------- #
# # # # # # # # # # # # # # # # # # # # # # # 

root = tk.Tk()
root.geometry("1300x700")
root.title("TissueTherm")
frame=tk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)
style0 = ttk.Style(root)
style0.theme_use("vista")

# # # # # # # # # # # # # # # # # # # # # # # # #
# ---------- Frame 1: Sample Details ---------- #
# # # # # # # # # # # # # # # # # # # # # # # # #

# Create and place frame 1
frame1 = ttk.LabelFrame(frame, text='1. Sample Details')
style1 = ttk.Style(frame1)
style1.theme_use("vista")
frame1.grid(row = 1, column = 0, sticky = 'news')

# Sample shape input
sample_shape = ttk.Label(frame1, text='Sample Shape:')
sample_shape.grid(row=0, column=0, pady=5)
shape = tk.StringVar()
sampleShape_comboBox = ttk.Combobox(frame1, values=["Square/Rectangle", "Circle/Ellipsoid"], textvariable=shape)
sampleShape_comboBox.grid(row=0, column=1, padx=3)
sampleShape_comboBox.bind("<<ComboboxSelected>>")

# Sample length input
len = ttk.Label(frame1, text="Length (mm):")
len.grid(row=1, column=0, pady=5)
len_var = tk.DoubleVar(value=135)
len_entry = ttk.Entry(frame1, textvariable=len_var)
len_entry.grid(row=1, column=1, padx=3)

# Sample width input
width = ttk.Label(frame1, text="Width (mm):")
width.grid(row=2, column=0, pady=5)
width_var = tk.DoubleVar(value=135)
width_entry = ttk.Entry(frame1, textvariable=width_var)
width_entry.grid(row=2, column=1, padx=3)

# Sample height input
height = ttk.Label(frame1, text="Height (mm):")
height.grid(row=3, column=0, pady=5)
height_var = tk.DoubleVar(value=40)
height_entry = ttk.Entry(frame1, textvariable=height_var)
height_entry.grid(row=3, column=1, padx=3)


def read_to_csv(stop_flag):
    global sec
    if not stop_flag:
        if not queue.empty():
            data = queue.get()

            with open(temps_file, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(data)
                sec += 3
            
            if sec > 15:
                stop_flag = True


        root.after(3000, read_to_csv, stop_flag)



        

inform_option = ttk.Label(frame1, text = "No option chosen")
inform_option.grid(row=7, column=0, pady=5, columnspan=3, sticky = 'w')

def start_readData(queue):
    global temps_file

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename = f"temperatureReadings_{timestamp}.csv"
    # initialize header of file to write to
    if not os.path.isfile(filename):
        with open(filename, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            temps_file = filename
            headerList = ['Time (s)', 'RTD1 (F)', 'RTD2 (F)', 'RTD3 (F)', 'RTD4 (F)', 'RTD5 (F)', 'RTD6 (F)', 
                            'RTD7 (F)', 'RTD8 (F)', 'RTD9 (F)', 'RTD10 (F)', 'RTD11 (F)', 'RTD12 (F)']
            writer.writerow(headerList)

    if 'temps_file' in globals() and temps_file != '':
        inform_option.config(text="Writing to file: " + os.path.basename(temps_file))
    
    readData_thread = threading.Thread(target=readData, args=(queue,))
    readData_thread.daemon = True
    readData_thread.start()



def upload_temps():
    global temps_file
    temps_file = tk.filedialog.askopenfilename()
    if 'temps_file' in globals() and temps_file != '':
        inform_option.config(text="Uploaded File: " + os.path.basename(temps_file))

separator = ttk.Label(frame1, text = "- - - - - - - - - - Data Collection Method - - - - - - - - - - -")
separator.grid(row=4, column=0, columnspan=3, sticky = 'news')

begin_label = ttk.Label(frame1, text="Option 1: ")
begin_label.grid(row=5, column=0)
# Begin Data Readings button
data_button = ttk.Button(frame1, text = 'Begin Data Readings', command=lambda: start_readData(queue)) 

data_button.grid(row = 5, column=1, sticky = 'w')
upload_label = ttk.Label(frame1, text ="Option 2: ")
upload_label.grid(row=6, column=0, pady=5)
# Upload File button
upload_button = ttk.Button(frame1, text='Upload File', command = upload_temps)
upload_button.grid(row=6, column=1, pady=5, sticky = 'w')



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ---------- Frame 2: Thermal Output Options ---------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Create and place frame 2
frame2 = ttk.LabelFrame(frame, text="2. Thermal Output Options")
style2 = ttk.Style(frame2)
style2.theme_use("vista")
frame2.grid(row=1, column=1, sticky='news')

lowRange = tk.DoubleVar()
lowRange.set(60)
highRange = tk.DoubleVar()
highRange.set(80)
range_label = ttk.Label(frame2, text="Temperature Range (F): ")
range_label.grid(row=0, column=0, columnspan=2, sticky = 'w')
lowRange_inp = ttk.Entry(frame2, textvariable = lowRange, width = 7)
lowRange_inp.grid(row=1, column=0, sticky = 'e')
transition = ttk.Label(frame2, text = "to")
transition.grid(row=1, column=1, sticky = 'w')
highRange_inp = ttk.Entry(frame2, textvariable = highRange, width=7)
highRange_inp.grid(row=1, column=2, sticky = 'news')

# 3D Thermal Map check button
therm_check = tk.IntVar()
thermal_map = ttk.Checkbutton(frame2, text='3D Thermal Map', variable = therm_check)
thermal_map.grid(row=2, column=0, sticky = 'w', pady=10)

# Temperature Table check button
temp_check = tk.IntVar()
thermal_table = ttk.Checkbutton(frame2, text='Temperature Table', variable = temp_check)
thermal_table.grid(row=4, column=0, sticky = 'w', pady=10)

def save_animation(anim1):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    output_file = f"3D-thermalAnimation_{timestamp}.mp4"
    write = animation.FFMpegWriter(fps=1)
    anim1.save(output_file, writer=write)
    
# initialize if graphs generated
tm_gen = False
tt_gen = False

# Function to display the thermal outputs
def display_therm():
    global tm_gen
    global tt_gen
    global fig1
    global anim1
    global temps_file
    # initialize no labels on the graph
    label_bool = tk.BooleanVar()
    label_bool.set(False)

    # update label_bool continously 
    def toggle_labels():
        show_labels = label_bool.get()
        return show_labels
    
    if 'temps_file' not in globals() or temps_file == '':
        messagebox.showerror("Error", "No file uploaded")
    else:

        if therm_check.get() == 0 and temp_check.get() == 0:
            messagebox.showerror("Error", "No thermal output selected")
        # if the 3D thermal map checkbox is selected
        if therm_check.get() == 1:
            # if thermal map has already been generated, check for reset and plot again
            if tm_gen:
                if messagebox.askokcancel("Warning", "Generating the graph will reset the animation. Do you want to proceed?"):
                    tm_gen = False
                    # get sample inputs
                    selected_shape = shape.get()
                    l = len_var.get()
                    w = width_var.get()
                    h = height_var.get()
                    if lowRange.get() > highRange.get():
                        messagebox.showerror("Error", "Low temperature cannot exceed high temperature")
                    else:
                        low = lowRange.get()
                        high = highRange.get()
                        # build frame for the 3D display
                        frame_3d = tk.LabelFrame(frame, text='3D Thermal Display', font=('Arial', 10))
                        frame_3d.grid(row=1, column=2, rowspan=3, sticky='news')
                        # call create_3d() from thermalMap.py and return animation objects
                        anim1, fig1, scat = tm.create_3d(selected_shape, l, w, h, low, high, temps_file)
                        save_button = ttk.Button(frame_3d, text = "Save Animation", command = lambda: save_animation(anim1))
                        save_button.grid(row=2, column=0, sticky = 'news', pady=5)
                        # create and place Show Labels checkbox
                        label_check = ttk.Checkbutton(frame2, text='Label Points', variable = label_bool, command=lambda: tm.update_labels(toggle_labels(), scat))
                        label_check.grid(row=3, column=0, sticky = 'e', pady=10)
                        

                        # place the animation in the tkinter frame
                        canvas1 = FigureCanvasTkAgg(fig1, master=frame_3d)
                        canvas1.draw()
                        canvas1.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky = 'news')
                        # set thermal map generation = true
                        tm_gen = True

            # else, plot 3d graph
            else:
                # get sample inputs
                selected_shape = shape.get()
                l = len_var.get()
                w = width_var.get()
                h = height_var.get()
                if lowRange.get() > highRange.get():
                    messagebox.showerror("Error", "Low temperature cannot exceed high temperature")
                else:
                    low = lowRange.get()
                    high = highRange.get()
                    # build frame for the 3D display
                    frame_3d = tk.LabelFrame(frame, text='3D Thermal Display', font=('Arial', 10))
                    frame_3d.grid(row=1, column=2, rowspan=3, sticky='news')
                    # call create_3d() from thermalMap.py and return animation objects
                    anim1, fig1, scat = tm.create_3d(selected_shape, l, w, h, low, high, temps_file)
                    save_button = ttk.Button(frame_3d, text = "Save Animation", command = lambda: save_animation(anim1))
                    save_button.grid(row=2, column=0, sticky = 'news', pady = 5)
                    # create and place Show Labels checkbox
                    label_check = ttk.Checkbutton(frame2, text='Label Points', variable = label_bool, command=lambda: tm.update_labels(toggle_labels(), scat))
                    label_check.grid(row=3, column=0, sticky = 'e', pady=10)                    
                    # place the animation in the tkinter frame
                    canvas1 = FigureCanvasTkAgg(fig1, master=frame_3d)
                    canvas1.draw()
                    canvas1.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky = 'news')
                    # set thermal map generation = true
                    tm_gen = True
                
        # if the temperature table checkbox is selected
        if temp_check.get() == 1:
            
            if tt_gen and therm_check.get() == 0:
                if messagebox.askokcancel("Warning", "Generating the graph will reset the animation. Do you want to proceed?"):
                    tt_gen = False
                    # build frame for the temperature table
                    frame6 = tk.LabelFrame(frame, text='Temperature Table', font=('Arial', 10))
                    frame6.grid(row=4, column=2, sticky='news')
                    # call update_table() from tempsTable.py
                    anim2, fig2 = tt.update_table(temps_file)
                    # place the animation in the tkinter frame
                    canvas2 = FigureCanvasTkAgg(fig2, master=frame6)
                    canvas2.draw()
                    canvas2.get_tk_widget().grid(row=4, column=2, sticky = 'news') 
                    tt_gen = True
            else:
                # build frame for the temperature table
                    frame6 = tk.LabelFrame(frame, text='Temperature Table', font=('Arial', 12))
                    frame6.grid(row=4, column=2, sticky='news')
                    # call update_table() from tempsTable.py
                    anim2, fig2 = tt.update_table(temps_file)
                    # place the animation in the tkinter frame
                    canvas2 = FigureCanvasTkAgg(fig2, master=frame6)
                    canvas2.draw()
                    canvas2.get_tk_widget().grid(row=4, column=2, sticky = 'news') 
                    tt_gen = True

    return tm_gen, tt_gen


# Generate Thermal Graph button - calls above display_therm() function
g_button = ttk.Button(frame2, text='Generate Thermal Graph', command=display_therm)
g_button.grid(row=5, column=0, columnspan=2)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ---------- Frame 3: E/H Field Orientation ---------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Create and place frame 3
frame3 = ttk.LabelFrame(frame, text="3. E/H Field Orientation")
style3 = ttk.Style(frame3)
style3.theme_use("vista")
frame3.grid(row=2, column=0, columnspan=2, sticky='news')

# Channel 1 checkboxes
ch1_var = tk.IntVar()
ch1_var.set(1)
ch1 = ttk.Label(frame3, text='Channel 1')
ch1.grid(row=0, column=0, sticky = 'w', padx=10)
ch1_e = ttk.Checkbutton(frame3, text='E-Field', variable = ch1_var, onvalue=1, offvalue=0)
ch1_e.grid(row=1, column=0, sticky = 'w', padx=10)
ch1_h = ttk.Checkbutton(frame3, text='H-Field', variable = ch1_var, onvalue=2, offvalue=0)
ch1_h.grid(row=2, column=0, sticky = 'w', padx=10)

# Channel 2 checkboxes
ch2_var = tk.IntVar()
ch2_var.set(1)
ch2 = ttk.Label(frame3, text='Channel 2')
ch2.grid(row=0, column=1, sticky = 'w', padx=10)
ch2_e = ttk.Checkbutton(frame3, text='E-Field', variable = ch2_var, onvalue=1, offvalue=0)
ch2_e.grid(row=1, column=1, sticky = 'w', padx=10)
ch2_h = ttk.Checkbutton(frame3, text='H-Field', variable = ch2_var, onvalue=2, offvalue=0)
ch2_h.grid(row=2, column=1, sticky = 'w', padx=10)

# Channel 3 checkboxes
ch3_var = tk.IntVar()
ch3_var.set(2)
ch3 = ttk.Label(frame3, text='Channel 3')
ch3.grid(row=0, column=2, sticky = 'w', padx=10)
ch3_e = ttk.Checkbutton(frame3, text='E-Field', variable = ch3_var, onvalue=1, offvalue=0)
ch3_e.grid(row=1, column=2, sticky = 'w', padx=10)
ch3_h = ttk.Checkbutton(frame3, text='H-Field', variable = ch3_var, onvalue=2, offvalue=0)
ch3_h.grid(row=2, column=2, sticky = 'w', padx=10)

# Channel 4 checkboxes
ch4_var = tk.IntVar()
ch4_var.set(2)
ch4 = ttk.Label(frame3, text='Channel 4')
ch4.grid(row=0, column=3, sticky = 'w', padx=10)
ch4_e = ttk.Checkbutton(frame3, text='E-Field', variable = ch4_var, onvalue=1, offvalue=0)
ch4_e.grid(row=1, column=3, sticky = 'w', padx=10)
ch4_h = ttk.Checkbutton(frame3, text='H-Field', variable = ch4_var, onvalue=2, offvalue=0)
ch4_h.grid(row=2, column=3, sticky = 'w', padx=10)

# Graph Display Options
eh_label = ttk.Label(frame3, text="Select Graph Display (one at a time)")
eh_label.grid(row=0, column=4, sticky = 'news')
eh_outp = tk.IntVar()
eh_outp.set(1)
e_graph = ttk.Checkbutton(frame3, text = "E-Field Strength vs Time", variable = eh_outp, onvalue=1, offvalue=0)
e_graph.grid(row= 1, column=4, sticky = 'w')
h_graph = ttk.Checkbutton(frame3, text = "H-Field Strength vs Time", variable = eh_outp, onvalue=2, offvalue=0)
h_graph.grid(row=2, column=4, sticky='w')

# function to display the file uploaded
def browse_file():
    global file_path 
    file_path = tk.filedialog.askopenfilename()
    if 'file_path' in globals() and file_path != '':
        file_label.config(text="Uploaded File:" +os.path.basename(file_path))

# Upload File button
browse_button = ttk.Button(frame3, text='Upload File', command=browse_file)
browse_button.grid(row=3, column=0, columnspan=2, sticky='news')
file_label = tk.Label(frame3, text = "No file uploaded")
file_label.grid(row=4, column=0, columnspan=5, sticky = 'w')

# function to plot the E-field or H-field graphs
def eh_generation():
    # error checking for a file
    if 'file_path' not in globals() or file_path == '':
        messagebox.showerror("Error", "No File Selected!")
    else:
        # get channel orientations
        ch1 = ch1_var.get()
        ch2 = ch2_var.get()
        ch3 = ch3_var.get()
        ch4 = ch4_var.get()
        channels = np.array([ch1, ch2, ch3, ch4])

        temp_errorCheck = False
        # error checking that the ports are oriented correctly
        if np.count_nonzero(channels == 1) == 1:
            messagebox.showerror("Error", "Not enough Electric Field ports selected (need 2)")
            temp_errorCheck = True
        if np.count_nonzero(channels == 2) == 1:
            messagebox.showerror("Error", "Not enough Magnetic Field ports selected (need 2)")
            temp_errorCheck = True
        if np.count_nonzero(channels == 1) == 3:
            messagebox.showerror("Error", "Too many Electric Field ports selected (need 2)")
            temp_errorCheck = True
        if np.count_nonzero(channels == 2) == 3:
            messagebox.showerror("Error", "Too many Magnetic Field ports selected (need 2)")
            temp_errorCheck = True 

        # if correct channel orientations provided, plot
        if np.count_nonzero(channels == 2) == 2 or np.count_nonzero(channels == 1) == 2:
            # if no graphs selected
            if eh_outp.get() == 0 and not temp_errorCheck:
                messagebox.showerror("Error", "No graph option selected")
            else:
                # create and place frame for the 2D plot
                frame_eh = tk.LabelFrame(frame, text='Field Strength vs Time', font=('Arial', 10))
                frame_eh.grid(row=3, column=0, columnspan=2, rowspan=2, sticky='news')
                #define which output to be displayed
                fig_opt = eh_outp.get()
                # call eh_plot() from eh_field.py to build the desired 2D plot
                fig_eh = eh_plot(file_path, ch1, ch2, ch3, ch4, fig_opt)
                # place the plot onto the frame
                canvas3 = FigureCanvasTkAgg(fig_eh, master=frame_eh)
                canvas3.draw()
                canvas3.get_tk_widget().grid(row=3, column=0, rowspan=2)
                #clear graph if different option chosen (storage issues)
                plt.close(fig_eh)
            
# Generate Field Strength Graph button - calls above eh_generation()
eh_button = ttk.Button(frame3, text='Generate Field Strength Graph', command = eh_generation)
eh_button.grid(row=3, column=3, columnspan=2, sticky = 'e')

# Space widgets uniformly
for widget in frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Double-check on closing
def on_closing():
    if messagebox.askyesno(title="Quit?", message = "Do you really want to quit?"):
        os.kill(os.getpid(), signal.SIGINT) # clear all scripts
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()
        root.destroy() # close tkinter frame
stop_flag = False

root.after(3000, read_to_csv, stop_flag)
root.mainloop()





