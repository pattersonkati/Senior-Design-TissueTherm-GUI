import serial

def readData(queue):
    second = 0
    sensor_data = []
    arduino = serial.Serial('COM4', 115200)

    while second <= 15:
        arduino_data = arduino.readline()
        dataString = arduino_data.decode('utf-8').strip()
        data = dataString[0:][:]

        readings = data.split(",")
        if len(readings) == 12:
            read_to_csv = [second, readings[0], readings[1], readings[2], readings[3], readings[4], readings[5],
                            readings[6], readings[7], readings[8], readings[9], readings[10], readings[11]]
            queue.put(read_to_csv)
            sensor_data.append(second)
            print(readings)
            second+= 3


