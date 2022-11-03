from typing import Union
import pyvisa as visa
import numpy as np

from waveform import waveform

class dataengine():

    def __init__(self, address: Union[None, str] = None, main_scale: str = '1.0E-6'):
        
        # find and open the oscillator
        self.rm = visa.ResourceManager()
        if address == None:
            resource_list = self.rm.list_resources()
            if len(resource_list) > 1:
                print('Warning: More than one device are detected.')
                print(f'Using resource: {resource_list[0]}')
            self.device = self.rm.open_resource(resource_list[0])
        else:
            self.device = self.rm.open_resource(address)
        
        # set the scale
        self.main_scale = main_scale
        self.device.write('horizontal:main:scale ' + self.main_scale)
        self.device.write('header off')

        # get parameters
        self.xincr = float(self.device.query('wfmpre:xincr?'))
        self.yoff  = float(self.device.query('wfmpre:yoff?'))
        self.ymult = float(self.device.query('wfmpre:ymult?'))
        self.yzero = float(self.device.query('wfmpre:yzero?'))
        self.xincr = float(self.device.query('wfmpre:xincr?'))

    def set_scale(self, new_scale: str):

        self.main_scale = new_scale
        self.device.write('horizontal:main:scale ' + self.main_scale)

        # update parameters
        self.xincr = float(self.device.query('wfmpre:xincr?'))
        self.yoff  = float(self.device.query('wfmpre:yoff?'))
        self.ymult = float(self.device.query('wfmpre:ymult?'))
        self.yzero = float(self.device.query('wfmpre:yzero?'))
        self.xincr = float(self.device.query('wfmpre:xincr?'))

    def get_data(self, wave: waveform):

        self.device.write('acquire:state on')
        y = self.device.query('curve?')
        y = np.array(y.split(',')).astype(np.float32)
        y = (y - self.yoff) * self.ymult + self.yzero
        wave.getdata(y)

# mock
if __name__ == '__main__':
    engine = dataengine()
    xincr = engine.xincr
    wave = waveform(time_line = xincr)
    engine.get_data(wave)
    print(wave.y)

                    

