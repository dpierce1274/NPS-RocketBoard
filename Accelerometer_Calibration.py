import adxl377
import time
from gpiozero import LED
import sys

acc = adxl377.ADXL377(busID=1, slaveAddr=0x48)
check_led = LED(19)

x_min = 3.0
y_min = 3.0
z_min = 3.0
x_max = 0.0
y_max = 0.0
z_max = 0.0
counter = 0.0


print('Calibration Commencing - Slowly rotate accelerometer about each axis when green light turns on')
time.sleep(2)

while True:
    try:
        counter += 1
        acc_data = acc.get_accel_values()
        x_value = float(acc_data[0])
        y_value = float(acc_data[1])
        z_value = float(acc_data[2])

        if counter > 100:
            print(acc_data)
            check_led.on()
            if x_value > x_max :
                x_max = x_value
            if x_value < x_min:
                x_min = x_value
            if y_value > y_max:
                y_max = y_value
            if y_value < y_min:
                y_min = y_value
            if z_value > z_max:
                z_max = z_value
            if z_value < z_min:
                z_min = z_value

        print('X Max: {:.4f}'.format(x_max), 'Y Max: {:.4f}'.format(y_max), 'Z Max: {:.4f}'.format(z_max))
        print('X Min: {:.4f}'.format(x_min), 'Y Min: {:.4f}'.format(y_min), 'Z Min: {:.4f}'.format(z_min))

    except KeyboardInterrupt:
        print('Final Calibration values:')
        print('X Max: {:.4f}'.format(x_max), 'Y Max: {:.4f}'.format(y_max), 'Z Max: {:.4f}'.format(z_max))
        print('X Min: {:.4f}'.format(x_min), 'Y Min: {:.4f}'.format(y_min), 'Z Min: {:.4f}'.format(z_min))
        sys.exit()

