def read_status_vfd():

       #import library related modules 
       import minimalmodbus
       import Modbus_setting_parameter as MSP
       from time import sleep
       import os
       import multiprocessing
       import psutil
       modbus_offset = 40001
       read_stat = 40201 - modbus_offset
       read_stat_power = 40214 - modbus_offset
       read_stat_motor_load_factor = 40224 - modbus_offset
       read_status_comulative_power = 40225 - modbus_offset
       read_stat_volt = 40203 - modbus_offset
       read_lenght = 2 
       #Create variable to reading
       read_stat1 = minimalmodbus.Instrument(MSP.USB_Port, MSP.Slave_Address)
       read_stat1.mode = minimalmodbus.MODE_RTU
       read_stat1.serial.parity = minimalmodbus.serial.PARITY_ODD
       read_stat1.serial.baudrate = MSP.Baudrate
       read_stat1.serial.bytesize = MSP.Bytesize
       read_stat1.serial.stopbits = MSP.Stopbits
       read_stat1.serial.timeout = MSP.Timeout
       read_stat1.clear_buffers_before_each_transaction = True
       read_stat1.close_port_after_each_call = True
       #Set while loop with try

       while True:	
              try:
                     data =read_stat1.read_registers(read_stat , read_lenght , functioncode=3) 
                     read_stat1.serial.close()
              
			## Split out the list into individual variables
                     hirz = data[0]
                     current = data[1]
                     volt = read_stat1.read_register(read_stat_volt ,0 , functioncode=3)
                     power = read_stat1.read_register(read_stat_power , 0 , functioncode=3)
                     motor_factor = read_stat1.read_register(read_stat_motor_load_factor , 0 ,functioncode=3)
                     Energy = read_stat1.read_register(read_status_comulative_power , 0 , functioncode=3)

                     rpm = int(482*(hirz*0.01)/51.56)
                    # pid1 = os.getpid()  # ??? Process ID (PID)
                    # core1 = psutil.Process(pid1).cpu_num()  # ??? Core ???????????????
                    # print(f"Status Display (PID: {pid1}) is running on Core {core1}")
                     #print("")
                     #print("------------------------------------------")
                     #print("Status VFD Real Time Moniter!!")
                     #print("------------------------------------------")
                     #print(f"Frequency      :  {float(hirz/100)} Hz")
                     #print(f"Current        :  {current/10} A")
                     #print(f"Output Voltage :  {volt * 0.1} V")
                     #print(f"DC Bus Voltage :  {bus}V")
                     #print(f"Total Power    :  {power/10} kW")
                     #print(f"Energy         :  {Energy * 0.01} kWh")
                     #print(f"Motor load     :  {motor_factor} %")
                     #print(f"Operation Code :  {process}")
                     #print("------------------------------------------")
                     #print("---------------------------------------------------------------")
                     #print(f"Current Operation:- {opp}")
                     #print("---------------------------------------------------------------")
                     #print("")
                     #print("")
                     #print("Press Ctrl+C to Change Settings Or Exit")

	              ## Refresh the command line table
                     #sleep(0.5)
                     #os.system('cls' if os.name == 'nt' else 'clear')
                     return [hirz , current , volt , power , rpm , motor_factor]
              
              except KeyboardInterrupt:
                     stop = read_stat1.write_register(8 , 0)
                     break
