import json
import ijson
import pandas as pd
import numpy as np


KEY_DICT = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B','C']
MODE_DICT = ['minor', 'major']


def import_json_file(file):
	with open(file,'r') as fp:
		data = json.load(fp)
	return data

def save_json_file(file, data):
	with open(file, 'w') as fp:
		json.dump(data, fp)

def import_ab(file):
	print 'Loading AB...'
	data = pd.read_csv(file, usecols=['recording_mbid', 'bpm', 'length', 'key_key', 'key_scale'], chunksize=1000)
	ab = dict()
	for chunk in data:
		for mbid, dur, key_key, key_scale, bpm in chunk.get_values():
			d = dict()
			d['bpm'] = bpm
			d['dur'] = dur
			d['key'] = key_to_str((key_key, key_scale))
			ab[mbid] = d	
	print 'Processed %i AB entries!!' % len(ab)
	return ab

def import_msd(file, key_conf):
	print 'Loading MSD...'
	data = import_json_file(file)
	print 'MSD loaded!!\nProcessing...'
	msd = dict()
	for k, d in data.iteritems():
		di = dict()
		di['bpm'] = d['tempo']
		di['dur'] = d['duration']
		di['key'] = []
		if (d['key_confidence'] >= key_conf and d['mode_confidence'] >= key_conf):
			di['key'] = key_to_str(key_format((d['key'], d['mode'])))	
		msd[k] = di
	print 'Processed %i MSD entries!!' % len(msd)
	return msd

def import_ids(file):
	print 'Loading IDS...'
	data = pd.read_csv(file, usecols=[0,1], names=['msd', 'mbid'], header=None)
	print 'IDS loaded!!\nProcessing...'
	ids = dict()
	for msd, mbid in data.get_values():
		ids[mbid] = msd
	print 'Processed %i IDS entries!!' % len(ids)
	return ids

def key_format(key):
	return [KEY_DICT[key[0]], MODE_DICT[key[1]]]

def key_to_str(key):
	k0 = str(key[0])
	k1 = str(key[1])
	if k0 == 'nan':
		k0 = 'C'
	if k1 == 'nan':
		k1 = 'major'
	return k0 + ' ' + k1

def import_msd_beats(file, beats_conf):
	print 'Loading MSD beats...'
	data = pd.read_csv(file, header=None, names=list(range(584)), chunksize=1000)
	beats = dict()
	for chunk  in data:
		for item in chunk.get_values():
			if item[1] == 'st':
				beats_st = item[2:]
			elif item[1] == 'con':
				b = np.array([beat for i,beat in enumerate(beats_st) if item[2+i]>beats_conf])
				beats[item[0]] = np.array(b)
	print 'Processed %i MSD beats instances...' % len(beats)
	return beats

def import_ab_beats(file):
	print 'Loading AB beats...'
	ab_beats = pd.read_csv(file, usecols=[1,2], names=['mbid', 'beats'], header=None, chunksize=1000)
	beats = dict()
	for chunk in ab_beats:
	    for mbid, b in chunk.get_values():
	        beats[mbid] = np.fromstring(b[1:-1], sep=',')
	print 'Processed %i AB beats instances...' % len(beats)
	return beats