import matplotlib.pyplot as pyplot
from tkinter import Tk
from tkinter import filedialog
import sys

pyplot.rcParams['font.sans-serif'] = "Times New Roman"
pyplot.rcParams['font.family'] = "sans-serif"

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
fp = open(filename, 'r')     # Open file in read mode

t = []
ACCx = []
ACCy = []
ACCz = []
accx = []
accy = []
accz = []
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
    alt.append(float(alt_reading[:-2]))

# Plot Results

pyplot.subplot(121)
pyplot.title('IMU Acceleration vs. Time', fontsize=15, weight='bold')
pyplot.plot(t[0:1200], ACCx[0:1200], t[0:1200], ACCy[0:1200], t[0:1200], ACCz[0:1200], linewidth=1)
pyplot.xlabel('Time (s)')
pyplot.ylabel('Acceleration (Gs)')
axis_labels = ['X-Axis', 'Y-Axis', 'Z-Axis']
pyplot.legend(axis_labels)


pyplot.subplot(122)
pyplot.title('Rotation vs. Time', fontsize=15, weight='bold')
pyplot.plot(t[0:1200], GRYx[0:1200], t[0:1200], GRYy[0:1200], t[0:1200], GRYz[0:1200], linewidth=1)
pyplot.xlabel('Time (s)')
pyplot.ylabel('Rotation Rate (deg/s)')
axis_labels = ['X-Axis', 'Y-Axis', 'Z-Axis']
pyplot.legend(axis_labels)

pyplot.figure(2)
pyplot.subplot(121)
pyplot.title('Altitude vs. Time', fontsize=15, weight='bold')
pyplot.plot(t, alt)
pyplot.xlabel('Time (s)')
pyplot.ylabel('Altitude (m)')


pyplot.subplot(122)
pyplot.title('Temperature vs. Time', fontsize=15, weight='bold')
pyplot.plot(t, temp)
pyplot.xlabel('Time (s)')
pyplot.ylabel('Temperature (deg C)')
pyplot.show()

