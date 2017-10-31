import os
import json
from essentia.standard import *
from essentia import pool
import numpy as np
from scipy.spatial import distance
from scipy.signal import medfilt
from sklearn.preprocessing import normalize
import matplotlib.pylab as plt


inputFile = 'Files/original/Sleeper.mp3'
midiFile = 'Files/original/Sleeper.mid'

JsonFile = 'Files/features/Sleeper_all.json'
JsonAggrFile = 'Files/features/Sleeper_aggr.json'
matrixFile = 'Files/features/Sleeper_mfccs_matrix.npy'
features_all = 'Files/features/features.json'

matrixPlotFile = 'Files/plots/matrix.pdf'
linePlotFile = 'Files/plots/line.pdf'


extractor = Extractor(dynamics = True,
                        dynamicsFrameSize = 88200,
                        dynamicsHopSize = 44100,
                        highLevel = True,
                        lowLevel = True,
                        lowLevelFrameSize = 4096,
                        lowLevelHopSize = 2048,
                        midLevel = True,
                        namespace = "",
                        relativeIoi = False,
                        rhythm = True,
                        sampleRate  = 44100,
                        tonalFrameSize  = 4096,
                        tonalHopSize = 2048,
                        tuning = True)

def extract(data):
    w = Windowing(type = 'hann')
    spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum

    loader = essentia.standard.MonoLoader(filename = data)
    audio = loader()
    pool = essentia.Pool()
    pool = extractor(audio)
    for frame in FrameGenerator(audio, frameSize = 4096, hopSize = 2048, startFromZero=False):
        pool.add('lowLevel.spectrum', spectrum(w(frame)))

    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
    YamlOutput(filename = JsonFile, format = "json")(pool)
    YamlOutput(filename = JsonAggrFile, format="json")(aggrPool)
    return pool

def compute_self_similarity(mfcc):
    print len(mfcc)
    matrix = []
    for i, frame in enumerate(mfcc):
        print i
        vector = [distance.euclidean(frame, frame2) for frame2 in mfcc]
        matrix.append(vector)
    return matrix

def plot_matrix(matrix, interpol=1):
    mat = [m[::interpol] for m in matrix[::interpol]]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(mat, interpolation='nearest', origin='lower', cmap=plt.cm.ocean)
    #plt.matshow(mat,origin='lower',cmap=plt.cm.ocean)
    plt.colorbar()
    plt.axis('off')
    plt.savefig(matrixPlotFile, bbox_inches='tight')
    plt.show()

def plot_line(pool):
    fig, ax = plt.subplots()
    energ = pool['lowLevel.spectral_energy']/np.linalg.norm(pool['lowLevel.spectral_energy'])
    ax.plot(medfilt(energ, 1001), 'k', label = 'Spectral Energy')
    comple = pool['lowLevel.spectral_complexity']/np.linalg.norm(pool['lowLevel.spectral_complexity'])
    ax.plot(medfilt(comple, 1001), 'r', label= 'Spectral Complexity')
    cent = pool['lowLevel.spectral_centroid']/np.linalg.norm(pool['lowLevel.spectral_centroid'])
    ax.plot(medfilt(cent, 1001), 'g', label = 'Spectral Centroid')
    crossi = pool['lowLevel.zerocrossingrate']/np.linalg.norm(pool['lowLevel.zerocrossingrate'])
    ax.plot(medfilt(crossi, 1001), 'b', label = 'Zero Crossing Rate')
    x = np.linspace(0,1,len(energ))
    beat = pool['rhythm.beats_loudness']
    xp = np.linspace(0,1,len(beat))
    beat = np.interp(x, xp, beat)
    beat = beat/np.linalg.norm(beat)
    ax.plot(medfilt(beat, 1001), 'y', label = 'Beats Loudness')

    plt.ylim([0, 0.0175])
    legend = ax.legend(loc='upper left', shadow=True)

    plt.savefig(linePlotFile, bbox_inches='tight')
    plt.show()



def main():
    pool = extract(inputFile)
    plot_line(pool)
    matrix = compute_self_similarity(pool['lowLevel.mfcc'])
    np.save(matrixFile, matrix)
    matrix = np.load(matrixFile)
    plot_matrix(matrix, interpol=2)


if __name__ == "__main__":
    main()