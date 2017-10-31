import essentia
import os
import json
from essentia.standard import *
from essentia import pool
import numpy as np


inputDir = '/home/marcsiq/SMC/aspma-lab/genre'


def fetchFiles(inputDir, descExt=".mp3"):
    files = []
    for path, dname, fnames  in os.walk(inputDir):
        for fname in fnames:
            if descExt in fname.lower():
                files.append((path, fname))
    return files


def extract_mfcc(data):
    w = Windowing(type = 'hann')
    spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
    mfcc = MFCC()

    for path, file in data:
        file_name, extension = os.path.splitext(file)
        file_location = path + "/" + file
        print file_location

        #computing mfcc
        loader = essentia.standard.MonoLoader(filename = file_location)
        audio = loader()
        pool = essentia.Pool()
        for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero=True):
            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
            pool.add('lowlevel.mfcc', mfcc_coeffs)
            pool.add('lowlevel.mfcc_bands', mfcc_bands)

        # saving Mfcc per frame.
        #YamlOutput(filename = path + "/"+ file_name + ".json", format = "json")(pool) t
       
        # saving Mfcc aggregated per audio file
        aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
        YamlOutput(filename = path + "/"+ file_name + ".json", format = "json")(aggrPool)



def main():
    data = fetchFiles(inputDir)
    extract_mfcc(data)


if __name__ == "__main__":
    main()