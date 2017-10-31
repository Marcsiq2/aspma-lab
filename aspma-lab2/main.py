from utils import *
from evaluate import *
import numpy as np
import pandas as pd
from mir_eval.key import weighted_score as key_eval
from mir_eval.beat import f_measure as beat_eval
from mir_eval.beat import trim_beats as beat_trim

AB_LOWLEVEL = 'Files/ab-2017-01-23-lowlevel-features.csv'
MSD_SUMMARY = 'Files/msd-2017-02-10-summary.json'
MBID_MSD = 'Files/msd-mbid-2016-01-results-ab.csv'


print "Preprocessing DATA..."
key_conf = 0.3
ab = import_ab(AB_LOWLEVEL)
msd = import_msd(MSD_SUMMARY, key_conf)
ids = import_ids(MBID_MSD)

dur_th = 0.05 #precision window for duration
mix = check_duration(ab, msd, ids, dur_th)
print 'Common elements: %i' % len(mix)


print "AB BPM vs MSD tempo accuracy 1"
bpm_th = 0.04 #precision window for bpm
correct1 = 0
correct2 = 0
for d1, d2 in mix:
    correct1 += compare(d1['bpm'], d2['bpm'], bpm_th)
    correct2 += compare(d2['bpm'], d1['bpm'], bpm_th)

print "IF WE TAKE MSD AS GROUNDTRUTH:"
print "Correct instances:\t%i" % (correct1)
print "Total instances:\t%i" % (len(mix))
print "Accuracy:\t\t%.4f\n" % (correct1/float(len(mix)))
print "IF WE TAKE AB AS GROUNDTRUTH:"
print "Correct instances:\t%i" % (correct2)
print "Total instances:\t%i" % (len(mix))
print "Accuracy:\t\t%.4f\n" % (correct2/float(len(mix)))


print "AB BPM vs MSD tempo accuracy 2"
bpm_th = 0.04 #precision window for bpm
correct1 = 0
correct2 = 0
for d1, d2 in mix:
    correct1 += adv_compare(d1['bpm'], d2['bpm'], bpm_th)
    correct2 += adv_compare(d2['bpm'], d1['bpm'], bpm_th)

print "IF WE TAKE MSB AS GROUNDTRUTH:"
print "Correct instances:\t%i" % (correct1)
print "Total instances:\t%i" % (len(mix))
print "Accuracy:\t\t%.4f\n" % (correct1/float(len(mix)))
print "IF WE TAKE AB AS GROUNDTRUTH:"
print "Correct instances:\t%i" % (correct2)
print "Total instances:\t%i" % (len(mix))
print "Accuracy:\t\t%.4f\n" % (correct2/float(len(mix)))

print "AB key vs MSD key"
score1 = []
score2 = []
for d1, d2 in mix:
    if d2['key']:
        score1.append(key_eval(d1['key'], d2['key']))
        score2.append(key_eval(d2['key'], d1['key']))
print "IF WE TAKE MSD AS GROUNDTRUTH:"
print "Total instances:\t%i" % (len(score1))
print "Score:\t\t\t%.4f\n" % (sum(score1)/float(len(score1)))
print "IF WE TAKE AB AS GROUNDTRUTH:"
print "Total instances:\t%i" % (len(score2))
print "Score:\t\t\t%.4f\n" % (sum(score2)/float(len(score2)))
