#coding:utf-8

# comparion two waveform


import sys
import os
import argparse
import numpy as np
from scipy import signal
from scipy.io.wavfile import read as wavread
from scipy.io.wavfile import write as wavwrite

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.16.3
#  scipy 1.4.1

def load_wav( path0, force_mono=False):
    # return 
    #        yg: wav data
    #        sr: sampling rate
    try:
        sr, y = wavread(path0)
    except:
        print ('error: wavread ', path0)
        sys.exit()
    else:
        yg= y / (2 ** 15)
        if force_mono :
            if yg.ndim == 2:  # if stereo
                yg= np.average(yg, axis=1)
    
    print ('file ', path0)
    print ('sampling rate ', sr)
    print ('length ', yg.shape)
    print ('yg.max', np.amax( np.abs(yg)))
    return yg,sr
    


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

def mean_subun(y1,y2):
    a1= np.mean(np.abs(y1 - np.mean(y1)))
    a2= np.mean(np.abs(y2 - np.mean(y2)))
    return ((a2 /a1) * (y1 - np.mean(y1)))- (y2 - np.mean(y2)) 
    

if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='comparison two waveforms')
    parser.add_argument('--wav_file1', '-s', default='test-output-rtwdf.wav', help='wav file name(16bit)')
    parser.add_argument('--wav_file2', '-f', default='test_overlapadd_out.wav', help='wav file name(16bit)')
    parser.add_argument('--offset', '-o', type=int, default=0, help='offset between two waveforms')
    args = parser.parse_args()
    
    
    path0= args.wav_file1
    yg,sr= load_wav(path0)
   
    path2= args.wav_file2
    yg2,sr2= load_wav(path2)
    
    seclen=120
    len0= int(sr * seclen)
    offset=args.offset
    print ('offset ', offset)
    
    yo= np.empty( ((len0-sr),2), dtype=float)
    yo[:,0]= yg[sr-offset: len0-offset , 0]
    yo[:,1]=yg2[sr: len0,  0]
    save_wav('comp.wav', yo, sr)
    
    
    yo[:,0]= mean_subun(yg[sr-offset: len0-offset , 0], yg2[sr: len0,  0])
    yo[:,1]= mean_subun(yg[sr-offset: len0-offset , 1], yg2[sr: len0,  1])
    save_wav('sabun_ola.wav', yo, sr)
    
