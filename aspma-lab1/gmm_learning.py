import os
import essentia
import os
import json
import random
from essentia.standard import *
from essentia import pool
import numpy as np
from sklearn import mixture
from sklearn import metrics

inputDir = '/home/marcsiq/SMC/aspma-lab/genre'

def fetchFiles(inputDir, descExt=".json"):
    files = []
    for path, dname, fnames  in os.walk(inputDir):
        for fname in fnames:
            if descExt in fname.lower():
                files.append((path, fname))
    return files

def collectMfcc(files):
    mfccs = dict()
    for path, fname in files:
        genre_clas = os.path.basename(os.path.normpath(path))
        pool = essentia.Pool()
        pool = YamlInput(filename = path + "/"+ fname, format = "json")()
        if genre_clas not in mfccs:
            mfccs[genre_clas] = []
        mfccs[genre_clas].append(pool)
    return mfccs

def computegmms(mfccs_train):
    gmms = dict()
    for genre in mfccs_train:
        os = []
        for pool in mfccs_train[genre]:
            #collect mfcc.mean withouth DC value
            mfcc_no0 = np.array(pool['lowlevel.mfcc.mean'][1:])
            os.append(mfcc_no0)
        gmms[genre] = mixture.GaussianMixture(n_components=1)
        gmms[genre].fit(os)
    return gmms

def computeScores(gmms, mfccs_test):
    correct = []
    predicted = []
    for genre in mfccs_test:
        correct_gen = 0.0
        samples_gen = 0.0
        for pool in mfccs_test[genre]:
            results = dict()
            for g in gmms:
                x = np.array(pool['lowlevel.mfcc.mean'][1:])
                x = x.reshape(1, -1)
                results[g] = gmms[g].score(x)
            predicted.append(max(results, key=results.get))
            correct.append(genre)
    print metrics.classification_report(correct, predicted)
    print metrics.confusion_matrix(correct, predicted)

  

def divide_dataset(db, train_percentage):
    # Get 'n_training_sounds_per_class' sounds per class 
    mfccs_train = dict()
    mfccs_test = dict()
    for class_name, sounds in db.items():
        sounds_class = sounds[:]
        train_per_class = int(np.ceil(len(sounds_class)*train_percentage))
        random.shuffle(sounds_class)
        mfccs_train[class_name] = sounds_class[:train_per_class]
        mfccs_test[class_name] = sounds_class[train_per_class:]

    print 'Created training and testing sets with the following number of sounds:\n\tTrain\tTest\tTotal\tClass'
    for class_name in mfccs_train:
        training_sounds = mfccs_train[class_name]
        testing_sounds = mfccs_test[class_name]
        print '\t%i\t%i\t%i\t%s' % (len(training_sounds), len(testing_sounds), len(db[class_name]), class_name)
    return mfccs_train, mfccs_test



def main():
    filenames = fetchFiles(inputDir)
    mfccs = collectMfcc(filenames)
    mfccs_train, mfccs_test = divide_dataset(mfccs, 0.9)
    gmms = computegmms(mfccs_train)
    computeScores(gmms, mfccs_test)

if __name__ == "__main__":
    main()