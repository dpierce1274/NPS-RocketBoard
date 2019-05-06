import traceback
import serial
import ublox
import time
import sys
import util


def main():

    ser = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.01)
    ubl = ublox.UBlox("spi:0.0", baudrate=5000000, timeout=0)
    util.check_apm()

    # Create data file and write header #
    tstr = time.strftime('%Y-%m-%d_%H-%M-%S-%Z.txt')
    filename = str('Telemetry Data ') + tstr

# Configure the GPS messages
    ubl.configure_solution_rate(rate_ms=500)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_POSLLH, 1)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_STATUS, 1)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_VELNED, 1)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_PVT, 1)

    message_names = ['NAV_POSLLH', 'NAV_STATUS', 'NAV_VELNED', 'NAV_PVT']

    check_msg = []

    while True:
        msg = ubl.receive_message()
        if msg is None:
            if opts.reopen:
                ubl.close()
                ubl = ublox.UBlox("spi:0.0", baudrate=5000000, timeout=0)
                continue
            print(empty)
            break
        if msg.name() == "NAV_STATUS":
            outstr = str(msg).split(",")[1:]
            fix_id = int(str_to_num(outstr[0]))  # GPS fix - from UBX-NAV-STATUS function
            fix_ok = int(str_to_num(outstr[2]))  # gpsFixOk (1 =  position and velocity valid and within DOP and ACC)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())
        if msg.name() == "NAV_POSLLH":
            outstr = str(msg).split(",")[1:]
            lon = float('%.7f' % (str_to_num(outstr[0])*10**-7))        # GPS longitude (deg)
            lat = float('%.7f' % (str_to_num(outstr[1])*10**-7))        # GPS latitude (deg)
            h_msl = float('%.1f' % (int(str_to_num(outstr[3])/1000)))   # GPS height MSL (m)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())
        if msg.name() == "NAV_VELNED":
            outstr = str(msg).split(",")[1:]
            gps_hdg = float('%.1f' % (str_to_num(outstr[5])*10**-5))    # GPS heading (deg)
            gps_gspd = int(str_to_num(outstr[4])/100)                   # GPS ground speed (m/s)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())
        if msg.name() == "NAV_PVT":
            outstr = str(msg).split(",")[1:]
            hour = outstr[4]
            min = outstr[5]
            sec = outstr[6]
            gps_time = '{}{}{}'.format(hour,min,sec)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())

        if all(elem in check_msg for elem in message_names):
            data = [gps_time, 'NAVMSG', time.time(), lat, lon, h_msl]
            write_to_file(filename, data)
            send_gps(ser, data)


def send_gps(ser, data):
    # This function formats and sends a GPS telemetry message to the ground radio
    # Inputs: GPS
    # Outputs: none
    msg = "{:>10s} {:>6s} {:>10d} {:>+9.5f} {:>+10.5f} deg {:>5d} m".format(data[0], data[1], int(data[2]), data[3],
                                                                            data[4], int(data[5]))
    ser.write('{:<100s}'.format('12 %s\r' % msg))
    print('{:<100s}'.format('12 %s\n' % msg))


def str_to_num(input):
    # This function converts a GPS string out value with equals sign to a float value
    # Inputs: String value with =
    # Outputs: Float value

    # Find the index of the equals sign
    index = input.find('=')

    # Remove all characters up to and including the equals sign
    output = input[index + 1:]

    output = float(output)

    return output


def write_to_file(filename, flt_params):
    # This function writes the flight parameters array to a .txt file on the SD Card
    # Input: flight parameters
    # Output: none
    fp = open(filename, 'a+')
    fp.write(str(flt_params) + '\n')
    fp.close()


start = time.time()

# Execute `main()` function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program Terminating...")
        time.sleep(1)
        sys.exit()
    except:                                                     # Pass and log all other errors
        s = traceback.format_exc()
        fp = open("GPS_Traceback_Log.txt", "a")
        fp.write(s + "\n")
        fp.close()