import serial  #import serial library

arduino_Serial_Data = serial.Serial('COM11',9600)
while (1==1):
    if (arduino_Serial_Data.inWaiting()>0):
        myData = str(arduino_Serial_Data.readline())
        #print(myData)
        x_start=int(myData.find("Identifier_for_variable_1"))

        y_start=int(myData.find(",Identifier_for_variable_2"))

        z_start=int(myData.find(",Identifier_for_variable_3"))
        t_start = int(myData.find(",Identifier_for_variable_4"))
        end=int(myData.find(",Identifier_for_variable_end"))
        x_accel = float(myData[x_start + len("X-axis = "):y_start])
        y_accel = float(myData[y_start + len(",Y-axis = "):z_start])
        z_accel = float(myData[z_start + len(",Z-axis = "):t_start])
        Current_time = float(myData[t_start + len(",Time = "):end])
        print(x_accel, y_accel, z_accel,Current_time)
        #Acc=myData.split(",")
        #print(Acc)