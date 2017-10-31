def compare(y_pred, y, threshold):
	diff = abs(y_pred - y)
	if diff < y*threshold:
		return True
	else:
		return False

def adv_compare(y_pred, y, threshold):
	if compare(y_pred, y, threshold):
		return True
	elif compare(y_pred*2, y, threshold):
		return True
	elif compare(y_pred/2, y, threshold):
		return True
	elif compare(y_pred*3, y, threshold):
		return True
	elif compare(y_pred/3, y, threshold):
		return True
	else:
		return False

def check_duration(ab, msd, ids, threshold):
	msdkeys = set(msd.keys())
	idskeys = set(ids.keys())

	mix = []

	for abk in ab.keys():
		if abk in idskeys:
			msdk = ids[abk]
			if msdk in msdkeys:
				if compare(ab[abk]['dur'], msd[msdk]['dur'], threshold):
					mix.append((ab[abk], msd[msdk]))
	return mix