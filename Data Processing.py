import matplotlib.pyplot as pyplot
from Tkinter import Tk
import tkFileDialog

pyplot.rcParams['font.sans-serif'] = "Times New Roman"
pyplot.rcParams['font.family'] = "sans-serif"

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = tkFileDialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
fp = open(filename, 'r')     # Open file in read mode

t = []
ACCx = []
ACCy = []
ACCz = []
GRYx = []
GRYy = []
GRYz = []
MAGx = []
MAGy = []
MAGz = []
temp = []
pres = []
alt = []

fp.readline()

for line in fp.readlines():
    cols = line.split(',')
    if len(t) == 0:
        start_time = float(cols[1])

    t.append(float(cols[1])-start_time)
    ACCx.append(float(cols[2]))
    ACCy.append(float(cols[3]))
    ACCz.append(float(cols[4]))
    GRYx.append(float(cols[5]))
    GRYy.append(float(cols[6]))
    GRYz.append(float(cols[7]))
    MAGx.append(float(cols[8]))
    MAGy.append(float(cols[9]))
    MAGz.append(float(cols[10]))
    temp.append(float(cols[11]))
    pres.append(float(cols[12]))
    alt_reading = cols[13]
    alt.append(float(alt_reading[0:5]))

# Plot Results
pyplot.title('Acceleration vs. Time', fontsize=15, weight='bold')
pyplot.plot(t, ACCx, t, ACCy, t, ACCz)
pyplot.xlabel('Time (s)')
pyplot.ylabel('Altitude (m)')
axis_labels = ['X-Axis', 'Y-Axis', 'Z-Axis']
pyplot.legend(axis_labels)
pyplot.show()