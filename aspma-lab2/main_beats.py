from utils import *
import numpy as np
from mir_eval.beat import f_measure as beat_eval

MBID_MSD = 'Files/msd-mbid-2016-01-results-ab.csv'
AB_BEATS = 'Files/ab-2017-01-23-beats.csv'
MSD_BEATS = 'Files/msd-2017-02-10-beats-rounded.csv'

ids = import_ids(MBID_MSD)
ab_beats = import_ab_beats(AB_BEATS)
msd_beats = import_msd_beats(MSD_BEATS, beats_conf=0.3)

idskeys = set(ids.keys())
msdkeys = set(msd_beats.keys())
score1 = []
score2 = []
for mbid in ab_beats:
    if mbid in idskeys:
        msdk = ids[mbid]
        if msdk in msdkeys:
            b1 = ab_beats[mbid]
            b2 = np.array(msd_beats[msdk])
            score1.append(beat_eval(b1, b2))
            score2.append(beat_eval(b2, b1))

print 'IF WE TAKE MSD AS GROUND TRUTH'
print "Total instances:\t%i" % (len(score1))
print 'F_score:\t\t%.4f\n' % (sum(score1) / float(len(score1)))

print 'IF WE TAKE AB AS GROUND TRUTH'  
print "Total instances:\t%i" % (len(score2))
print 'F_score:\t\t%.4f\n' % (sum(score2) / float(len(score2)))