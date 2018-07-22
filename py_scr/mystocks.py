#!/usr/bin/python
#usage script_name <portofolio.txt>
import os
import json
import urllib
import sys
import time

def get_url(symbol_list):
	#print 'calling get_price for ' + symbol
	url = 'https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols='+symbol_list+'&apikey=REGISTER_TO_GET&datatype=json'	
	fp = urllib.urlopen(url)
	data = fp.read()
	decoded_data = data.decode("utf8")
	fp.close()
	parsed_data = json.loads(decoded_data)
	data_str = parsed_data['Stock Quotes']
	return data_str

def get_price(symbol,url_data,price_key):
	sym = symbol.upper()
	for dic_item in url_data:
		for key in dic_item:
			val = dic_item[key]
			if val.find(sym) != -1:
				price = dic_item.get(price_key,'0.0')
				return float(price)
	return float("0")


def display_result(fname,stk_prop):
	dash = '-' * 82
	totalcost = 0 
	totalval = 0
	totalgain = 0
	print('{:<20s}{:>4s}{:>10s}{:>10s}{:>10s}{:>10s}{:>8s}{:>10s}'.format(fname.capitalize(),'Qty','Cost','Total','Crnt Val','Acquired','%incr','Return'))
	print dash
	for stock in stk_prop:
		totalcost = totalcost + stk_prop[stock][3]
		totalval = totalval + stk_prop[stock][4]
		print('{:<20s}{:>4d}{:>10.2f}{:>10.2f}{:>10.2f}{:>10.2f}{:>8.2f}{:>10.2f}'.format(stk_prop[stock][6],stk_prop[stock][0],stk_prop[stock][3],stk_prop[stock][4],stk_prop[stock][2],stk_prop[stock][1],stk_prop[stock][5],stk_prop[stock][4] - stk_prop[stock][3])) 
	print dash
	print('{:<20s}{:>4s}{:>10.2f}{:>10.2f}{:>38.2f}'.format('Agregate','',totalcost,totalval,totalval-totalcost))
	print dash
	
		
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'usage: ' +  sys.argv[0] + ' filename+'
		exit(-1)
	nargs = 1
	cache_data = {}
	try:
		df =  open('daily_cache','r') 
		for line in df:
			k,v = line.rstrip().split(':')
			cache_data[k] = v
	except:
		df =  open('daily_cache','a') 
		print 'No cache file .. creating one'
	finally:
		df.close()
	print 'cache file .. append mode'
	df =  open('daily_cache','a') 
	df.seek(2)
	while nargs < len(sys.argv):
		fname = sys.argv[nargs]
		nargs += 1
		slist = []
		stk_prop = {} 
		with open(fname,'r') as f:
			for line in f:
				symb,qty,price,desc = line.split(':')
				desc=desc.replace('\n','')
				slist.append(symb)
				stk_prop[symb] = [ int(qty), float(price), 0.0,float(qty) * float(price),0.0,0.0,desc]
		sym_list = ",".join(slist)
		url_data = get_url(sym_list)
		for stk in slist:
			update_cache = 0
			if cache_data.get(stk) != None:
				current_price = float(cache_data.get(stk))
			else:
				print 'NO cache data found for ' + stk
				current_price = get_price(stk,url_data,'2. price')
				cache_data[stk] = current_price
				print 'New data for ' + stk + 'current price ' + str(current_price)
				update_cache = 1
			#update symbol tuple
			if current_price != 0:
				cv = current_price * stk_prop[stk][0]
				pp = stk_prop[stk][3]
				stk_prop[stk][2] = current_price
				stk_prop[stk][4] = cv
				stk_prop[stk][5] = ((cv - pp)* 100.0)/(pp)
			if update_cache != 0:
				try:
					df.write('%s:%s\n'%(stk,cache_data[stk]))
					print 'Updated cache data'
				except:
					df.close()
		display_result(fname,stk_prop)
	df.close()
	


