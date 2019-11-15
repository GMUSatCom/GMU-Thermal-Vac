from time import sleep
from mcculw import ul
from mcculw.enums import *
import math
import pandas as pd


# template of the dataframe for pandas datalogging
data_template = {
    'time':[],
    'Millivolts':[],
    'Voltage':[],
    'Celsius':[],
}

# Board & Channel Constants
BOARD_NUM = 0

DIO_0 = 0
DIO_1 = 1
DIO_2 = 2

CH_0 = 0


###### Initialize the USB-202
def init():
    # Create device object based on USB-202
    ul.ignore_instacal()
    device = ul.get_daq_device_inventory(InterfaceType.ANY)
    ul.create_daq_device(BOARD_NUM, device[0])



###### Initialize digital output pins
def init_digital():
    # All 8 bits in Port 1 set as input by default -> set to output
    ul.d_config_port(BOARD_NUM, DigitalPortType.AUXPORT, DigitalIODirection.OUT)

#initializes an empty dataframe based on given template
def init_DataFrame(template):
    df = pd.DataFrame(template)
    return df

###### Set digital output DIO_0 to val (val is 1 for high and 0 for low)
def digital_write(val):
    # Write val to DIO_0
    ul.d_bit_out(BOARD_NUM, DigitalPortType.AUXPORT, DIO_0, val)



###### Get analog input from CH0 as mV
def analog_read():
    return ul.a_in(BOARD_NUM, CH_0, ULRange.BIP5VOLTS)
    # return input value from CH0
    # return ul.to_eng_units(BOARD_NUM, ULRange.BIP10VOLTS, ul.a_in(BOARD_NUM, CH_0, ULRange.BIP5VOLTS))



# convert analog voltage(mV) read to a temperature celsius
def convert_mV_to_C(analog_input):
    base_voltage = 2230.8
    #magic numbers from datasheet
    unknown = 13.582
    unknown2 = 0.00433
    #equation 2 from spec sheet for lht87 sensors
    converted_val = ((unknown-(math.sqrt(math.pow(unknown, 2) + 4 * unknown2 * (base_voltage - analog_input*1000))))/(2 * (-1 * unknown2))) + 30
    return converted_val



# log one data sample to the main dataframe
def log_data(dataframe):
    mV_reading = analog_read()#avoid running more than 1 read for logging
    data = {'time':pd.datetime.now(), 'Millivolts':mV_reading, 'Voltage':(mV_reading), 'Celsius':convert_mV_to_C(mV_reading)}

    dataframe = dataframe.append(data, ignore_index = True)
    return dataframe

#return number of test intervals for time period inputted as seconds, sample_freq is time between samples
def test_length(sample_freq):
    raw_inp = int(input("enter test duration time (sec): "))
    return int(raw_inp / sample_freq)

### Main Function
def main():
    init()
    init_digital()
    df = init_DataFrame(data_template)

    for i in range(test_length(0.05)):
        sleep(0.05)
        df = log_data(df)
        
        
    #convert to csv    
    df.to_csv('./desktop/data.csv', index = False)

'''    
    digital_write(1)
    sleep(1)
    digital_write(0)

    sleep(0.5)
    print("Analog Input: ", analog_read())
    sleep(0.5)
'''
if __name__ == "__main__":
    main()