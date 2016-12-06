var MongoClient = require('mongodb').MongoClient, assert = require('assert');

var url = 'mongodb://localhost:27017/test';


var map = function() {
   var stop = ('de','la','les','à','alors','au','aucuns','aussi','autre','avant','avec','avoir','bon','car',
		'ce','cela','ces','ceux','chaque','ci','comme','comment','dans','des','du','dedans','dehors',
		'depuis','devrait','doit','donc','dos','début','elle','elles','en','encore','essai','est','et',
		'eu','fait','faites','fois','font','hors','ici','il','ils','je','juste','la','le','les','leur',
		'là','ma','maintenant','mais','mes','mine','moins','mon','mot','même','ni','nommés','notre','nous','ou',
		'où','par','parce','pas','peut','peu','plupart','pour','pourquoi','quand','que','quel','quelle','quelles',
		'quels','qui','sa','sans','ses','seulement','si','sien','son','sont','sous','soyez','sujet','sur','ta',
		'tandis','tellement','tels','tes','ton','tous','tout','trop','très','tu','voient','vont','votre','vous','vu',
		'ça','étaient','état','étions','été','être')  
    var text = this.text;
    if (text) { 
        text = text.toLowerCase().replace("rt","").replace("francoisfillon","fillon").replace("nicolassarkozy","sarkozy")
	.replace(/[.,\/#@!$%\^&\*;:{}=\-_`~()]/g,"")
	.replace("alainjuppe","juppe").replace("brunolemaire","lemaire").replace("juppé","juppe").replace("vivementjuppe","juppe")
	.replace("jfpoisson78","poisson").replace("jfcope","cope").replace("copé","cope").replace("sarko ","sarkozy")
	.replace("bruno","lemaire").replace("vivementjuppé","juppe")
	.split(" "); 
        for (var i = text.length - 1; i >= 0; i--) {
            if (text[i])  
	    {
               emit(text[i].toString(), 1);
            }
        }
    }
};

var reduce = function( key, values ) {    
    var count = 0;    
    values.forEach(function(v) {            
        count +=v;    
    });
    return count;
}

// Use connect method to connect to the server
MongoClient.connect(url, function(err, db) 
{
  assert.equal(null, err);
  console.log("Connected successfully to server");
  var collection = db.collection("tweets");
  collection.mapReduce(map, reduce, {out: "word_count"})
  var new_collection = db.collection("word_count")
  var result =	new_collection.find({"_id":{$in:["fillon","sarkozy","juppe","nkm","lemaire","poisson","coppe"]}}).sort({value:-1})
  .toArray(function(err,docs) 
  {
    assert.equal(err, null);
    console.log("Found the following records");
    console.log(docs);
  });
  db.close();
});



