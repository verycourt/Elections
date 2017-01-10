import pandas as pd
import re

# open the file
data = open("debat_primaire_droite_24_11_16/test3.json", "r")

# get the whole document (it is one line)
dataSplit = data.readline().split('}{')

# Suppress first and last curly brackets

# /-1  suppress unicode
dataSplit = [x.replace('\': u\'', '\': \'') for x in dataSplit]

# 0.1/ replace single quotes of keys by double quotes

# keysTw = ['\'t_text\'', '\'t_lng\'', '\'t_lat\'', '\'t_time\'', '\'t_state\'']
# dataSplit = [x.replace(y, y.replace('\'', '\"')) for y in keysTw for x in dataSplit]
dataSplit = [x.replace('\'t_text\'', '\"t_text\"')
	.replace('\'t_lng\'', '\"t_lng\"')
	.replace('\'t_lat\'', '\"t_lat\"')
	.replace('\'t_time\'', '\"t_time\"')
	.replace('\'t_state\'', '\"t_state\"')
	.replace('\'\'', '\"\"')
	 for x in dataSplit]

# 0.2/ do the same for the timestamp

# compiler finds the timestamps
compiler = re.compile(r'(\'[0-9]*\')')

for tweet in dataSplit:
	# result lists the timestamp of current tweet ( len(result) = 1 )
	tmp = compiler.findall(tweet)
	# split tweet before/after the timestamp
	tweetSplit = tweet.split(tmp[0])
	# correct the timestamp
	finalTmp = re.sub(r'\'', '\"', tmp[0])
	# correct the whole tweet if only one timestamp is in the tweet
	if len(tmp) == 1:
		tweet = tweetSplit[0] + finalTmp + tweetSplit[1]
	else:
		# nullify the tweet if multiple timstamps detected
		tweet = {"t_text": "", "t_lng": 0.0, "t_lat": 0.0, "t_time": "", "t_state": ""}
	print(tweet)
	break


# 1/ Put backslash before double quote inside a value (cf key/value system)
# AFTER

# 2/ Put backslash before backslash, then before slashes
dataSplit = [x.replace('\\', '\\\\').replace('/', '\\/') for x in dataSplit]


# 3/ change single quotes surrounding values into double quotes

