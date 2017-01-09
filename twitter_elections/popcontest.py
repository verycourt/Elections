#!/usr/bin/python
import pymongo
from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet
candidates = ['valls','macron','mlp','jadot','melenchon','bayrou','poutou','peillon','rugy','hamon','pinel','benhamias','montebourg','fillon']
pseudo = {'valls':['valls','@manuelvalls','#valls'],'macron':['macron','#macron','@EmmanuelMacron'],'jadot':['Jadot','#Jadot','@yjadot'],
'mlp':['@MLP_officiel','#MLP','lepen'],'melenchon':['Melenchon','#Melenchon','@JLMelechon'],'bayrou':['Bayrou','#Bayrou','@bayrou'],
'poutou':['Poutou','#Poutou','@PhilippePoutou'],'peillon':['Peillon','#peillon','@Vincent_Peillon'],'rugy':['#Rugy','Rugy','@FdeRugy'],
'hamon':['Hamon','#hamon','@benoithamon'],'pinel':['pinel','#pinel','@SylviaPinel'],'benhamias':['bennhamias','#bennhamias','@JLBennhamias'],
'montebourg':['montebourg','#montebourg','@montebourg'],'fillon':['Fillon','#Fillon','@FrancoisFillon']}

for candidate in candidates:
	print(candidate)
	regexp = ''
	for p in pseudo[candidate]:
		regexp = regexp + p + "|"
	regexp = regexp[:-1]
	print(regexp)
	pipe = [{"$match":{"t_text":{"$regex":regexp}}},{"$group":{"_id":candidate,"total":{"$sum":1}}}]
	#pipe = [{"$match":{"t_text":{"$regex":candidate}}},{"$group":{"_id":candidate,"total":{"$sum":1}}}]
	pprint(list(collection.aggregate(pipeline=pipe)))
