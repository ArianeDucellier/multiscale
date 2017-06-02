#/bin/python
import numpy as np
import sys
import os
import obspy
from obspy.core import read, Stream, Trace
import pylab as plt
from obspy.signal.invsim import cosine_sac_taper
from obspy.signal.util import _npts2nfft
from scipy.signal import freqz,butter,buttord,lfilter,filtfilt



def butter_bandpass(filt_freq,fs):
    nyq = 0.5 * fs

    wp=[filt_freq[1]/nyq, filt_freq[2]/nyq, ]
    ws=[filt_freq[0]/nyq, filt_freq[3]/nyq]
    N, wn = buttord(wp, ws, 3, 16)
    print N
    b, a = butter(N, wn, btype='band')
    return b, a


def flex_cut_trace(tr, cut_starttime, cut_endtime):
    # not cut strictly, but also based on the original trace length
    if not isinstance(tr, obspy.Trace):
        raise ValueError("cut_trace method only accepts obspy.Trace"
                "as the first argument")

    starttime = tr.stats.starttime
    endtime = tr.stats.endtime
    cut_starttime = max(starttime, cut_starttime)
    cut_endtime = min(endtime, cut_endtime)
    if cut_starttime > cut_endtime:
        raise ValueError("Cut starttime is larger than cut endtime")
    return tr.slice(cut_starttime, cut_endtime)

def cut_func(st, cut_start, cut_end, dynamic_length=10.0):
        t1 = cut_start - dynamic_length
        t2 = cut_start + dynamic_length
        if isinstance(st, obspy.Trace):
            return flex_cut_trace(st, t1, t2)
        elif isinstance(st, obspy.Stream):
            tr_list = []
            
        for tr in st:
            tr_list.append(flex_cut_trace(tr, t1, t2))
            return obspy.Stream(traces=tr_list)
        else:
            raise ValueError("cut_func method only accepts obspy.Trace or"                                                                                                                                                             "obspy.Stream as the first Argument")

def filter_synt(tr, pre_filt):
    """
    Perform a frequency domain taper like during the response removal
    just without an actual response...
    :param tr:
    :param pre_filt:
    :return:
    """

    data = tr.data.astype(np.float64)
    # smart calculation of nfft dodging large primes
    nfft = _npts2nfft(len(data))
    fy = 1.0 / (tr.stats.delta * 2.0)
    freqs = np.linspace(0, fy, nfft // 2 + 1)
    # Transform data to Frequency domain
    data = np.fft.rfft(data, n=nfft)
    data *= cosine_sac_taper(freqs, flimit=pre_filt)
    data[-1] = abs(data[-1]) + 0.0j
    # transform data back into the time domain
    data = np.fft.irfft(data)[0:len(data)]
    # assign processed data and store processing information
    tr.data = data

def write_su_file(filename,stream) : 

    stream.write(filename,format='SU')

def read_su_file(filename):
    stream=read(filename,format='SU')
    return stream


def process_syn(stream,starttime,endtime,sampling_rate,npts,filt_freq,max_percentage=0.05) :

    stream_process = Stream()
    for tr in stream :
        new_tr=tr.copy()
        cut_func(new_tr, starttime, endtime)

        # detrend, demean, taper
        new_tr.detrend("linear")
        new_tr.detrend("demean")
        new_tr.taper(max_percentage=max_percentage, type="hann")

        # geometric compensation
        # filter and interpolation
        filter_synt(new_tr, filt_freq)
        new_tr.interpolate(sampling_rate=sampling_rate,\
                starttime=new_tr.stats.starttime,npts=npts)

        # detrend, demean, taper
        new_tr.detrend("linear")
        new_tr.detrend("demean")
        new_tr.taper(max_percentage=max_percentage, type="hann")

        new_tr.data = np.require(new_tr.data, dtype=np.float32)
        stream_process.append(new_tr)

    return stream_process


if __name__ == '__main__':    


    inputfile = sys.argv[1] 

    # read syn 
    stream=read_su_file(inputfile)

    print 'input data, ntr/npts/deltat:', len(stream), len(stream[0]), stream[0].stats.delta

    # process syn
    npts=6001
    sampling_rate=10000.0
    starttime=0
    endtime=0.6
    filt_freq=[2,4,20,25]

    stream_process_syn=process_syn(stream,starttime,endtime,
                        sampling_rate,npts,filt_freq,max_percentage=0.8)
    
    print 'output data, ntr/npts/deltat:', len(stream_process_syn), \
            len(stream_process_syn[0]), stream_process_syn[0].stats.delta

    plot=True
    if plot:
        fig = plt.figure(figsize=(15,3))
        ax = fig.add_subplot(211)
        tmp_t = np.linspace(0, stream[0].stats.npts/stream[0].stats.sampling_rate,
                            stream[0].stats.npts)
        plt.plot(tmp_t,stream[0].data,'k',label='input',linewidth=1.5)
        plt.xlim([min(tmp_t),max(tmp_t)])
        plt.xlabel('time (s)')
        ax.grid(True)

        ax = fig.add_subplot(212)
        tmp_t = np.linspace(0, npts / sampling_rate, npts)
        plt.plot(tmp_t,stream_process_syn[0],'k',label='processed',linewidth=1.5)
        plt.xlim([min(tmp_t),max(tmp_t)])
        plt.xlabel('time (s)')
        ax.grid(True)


        plt.show()




