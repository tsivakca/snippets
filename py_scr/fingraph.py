#!/usr/bin/python -t
import sys
import json
import time
import urllib
import os
import matplotlib.pyplot as plt

val = {}
def get_cache_data(symbol):
	path = os.getcwd() + '/data/'
	fname = path+'data.'+symbol
	try:
		with open(fname,'r') as f:
			data=f.read()
		f.close()
	except:
		print 'cache file does not exit.. fetching from url'
		return None
	decoded_data = data.decode("utf8")
	parsed_data = json.loads(decoded_data)
	data_str = parsed_data['Time Series (Daily)']
	return data_str

def get_daily_url(symbol):
	data_str = get_cache_data(symbol)
	path = os.getcwd() + '/data/'
	if data_str is None:
		fname = path+'data.'+symbol
		url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey=DBNYD5WNM68A3KRE&datatype=json'	
		fp = urllib.urlopen(url)
		data = fp.read()
		fp.close()
		decoded_data = data.decode("utf8")
		parsed_data = json.loads(decoded_data)
		data_str = parsed_data['Time Series (Daily)']
		with open(fname,'a') as fp:
			fp.write(data)
			print 'Storing data in cache .. '
		fp.close()
	return data_str

def process(dlist):
	#form tstring as a key
	ndict_item = len(dlist[0]) -1
	while  ndict_item >= 0 :
		date_key = time.time() - 86400 * ndict_item
		key = time.strftime('%Y-%m-%d',time.localtime(date_key))
		val[key] = 0	
		for d in dlist:
			if d.has_key(key) and val[key] != -1 :
				cv = d[key].get('4. close')
				val[key] = val[key] + float(cv) * int(qty_list[dlist.index(d)])
			else:
				val[key] = -1
		ndict_item = ndict_item - 1
	return val

def plot(val):
	nitems = len(val) -1
	xdata = []
	ydata = []
	while  nitems >= 0 :
		date_key = time.time() - 86400 * nitems *5
		key = time.strftime('%Y-%m-%d',time.localtime(date_key))
		if val.has_key(key):
			if val[key] != -1:
				xdata.append(key)
				ydata.append(val[key])
		nitems = nitems - 1
	print 'Last aggregated price' + str(ydata[len(ydata)-1])
	plt.plot(xdata,ydata)
	plt.show()

if __name__ == '__main__':
	dict_list = []
	qty_list = []
	if len(sys.argv) < 2:
		print 'usage: ' + sys.argv[0] + ' filename '
		print 'filename format:symbol:qty:price_paid:desc '
		exit(-1)
	with open(sys.argv[1],'r') as fp:
		for line in fp:
			sym,qty,pr,desc = line.split(':')
			dict_list.append(get_daily_url(sym))
			qty_list.append(qty)
	fp.close()
	process(dict_list)	
	plot(val)
