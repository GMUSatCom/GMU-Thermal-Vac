from time import sleep
from mcculw import ul
from mcculw.enums import *
import math

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



###### Set digital output DIO_0 to val (val is 1 for high and 0 for low)
def digital_write(val):
    # Write val to DIO_0
    ul.d_bit_out(BOARD_NUM, DigitalPortType.AUXPORT, DIO_0, val)



###### Get analog input from CH0
def analog_read():
    # return input value from CH0
    return ul.to_eng_units(BOARD_NUM, ULRange.BIP10VOLTS, ul.a_in(BOARD_NUM, CH_0, ULRange.BIP5VOLTS))

# convert analog voltage(mV) read to a temperature celsius
def convert_volt_to_c(analog_input):
    base_voltage = 2230.8
    unknown = 13.582
    unknown2 = 0.00433
    #function from spec sheet for lht87 sensors
    converted_val = ((unknown-(math.sqrt(math.pow(unknown, 2) + 4 * unknown2 * (base_voltage - analog_input))))/(2 * -unknown2)) + 30
    return converted_val

### Main Function
def main():
    init()


init_digital()

sleep(0.05)

while (1):
    print(analog_read())
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