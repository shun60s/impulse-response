#coding:utf-8

# make test input signal to get impulse response
#
#   test signal : 1sec-zeros + one pulse(any value) + 1sec-zeros


import sys
import argparse
import numpy as np
from scipy.io.wavfile import write as wavwrite

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.16.3
#  scipy 1.4.1

def save_wav( path0, data, sr=44100, normalize=False):
    #
    print ('file ', path0)
    
    amplitude = np.iinfo(np.int16).max
    max_data = np.amax(np.abs(data))  # normalize, max level is 16bit full bit
    if max_data <  (1.0 / amplitude):
        max_data=1.0
    
    try:
        if normalize :
            wavwrite(path0, sr, np.array( (amplitude / max_data) * data , dtype=np.int16))
        else:
            wavwrite(path0, sr, np.array( amplitude  * data , dtype=np.int16))
    except:
        print ('error: wavwrite ', path0)
        sys.exit()



if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='make test signal to get impulse response')
    parser.add_argument('--samplerate', '-s', default='44100', help='sampling rate')
    args = parser.parse_args()
    
    sr= int(args.samplerate)
    # overwrite sr
    #sr= 88200 
    
    data0=np.zeros( sr * 2)
    
    for v0 in  [1.0]:  # set each value of one pulse
        data0[sr]=v0
        path_out0='impulse_1sec_' +  str( int(v0*100)) + '_1sec_'+ str(sr) + '.wav'
        # write process output
        save_wav( path_out0, data0, sr)
    


