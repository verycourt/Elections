var rawData = {"columns":["Fran\u00e7ois Fillon","Manuel Valls"],"index":["samedi 17 d\u00e9cembre 2016","dimanche 18 d\u00e9cembre 2016","lundi 19 d\u00e9cembre 2016","mardi 20 d\u00e9cembre 2016","mercredi 21 d\u00e9cembre 2016","jeudi 22 d\u00e9cembre 2016","vendredi 23 d\u00e9cembre 2016","samedi 24 d\u00e9cembre 2016","dimanche 25 d\u00e9cembre 2016","lundi 26 d\u00e9cembre 2016","mardi 27 d\u00e9cembre 2016","mercredi 28 d\u00e9cembre 2016","jeudi 29 d\u00e9cembre 2016","vendredi 30 d\u00e9cembre 2016","samedi 31 d\u00e9cembre 2016","dimanche 1 janvier 2017","lundi 2 janvier 2017","mardi 3 janvier 2017","mercredi 4 janvier 2017","jeudi 5 janvier 2017","vendredi 6 janvier 2017","samedi 7 janvier 2017","dimanche 8 janvier 2017","lundi 9 janvier 2017","mardi 10 janvier 2017","mercredi 11 janvier 2017","jeudi 12 janvier 2017","vendredi 13 janvier 2017","samedi 14 janvier 2017"],"data":[["29","19"],["29","18"],["25","11"],["27","10"],["26","100"],["25","44"],["25","23"],["25","22"],["29","10"],["21","13"],["24","13"],["34","12"],["26","8"],["30","19"],["24","12"],["29","8"],["43","58"],["34","36"],["39","49"],["37","67"],["31","35"],["29","27"],["36","20"],["41","21"],["41","19"],["36","56"],["35","24"],["46","42"],["35","42"]]}
var rawData = {"columns":["Fran\u00e7ois Fillon","Manuel Valls"],"index":["17-01 19:40","17-01 19:48","17-01 19:56","17-01 20:04","17-01 20:12","17-01 20:20","17-01 20:28","17-01 20:36","17-01 20:44","17-01 20:52","17-01 21:00","17-01 21:08","17-01 21:16","17-01 21:24","17-01 21:32","17-01 21:40","17-01 21:48","17-01 21:56","17-01 22:04","17-01 22:12","17-01 22:20","17-01 22:28","17-01 22:36","17-01 22:44","17-01 22:52","17-01 23:00","17-01 23:08","17-01 23:16"],"data":[["2","60"],["2","62"],["3","100"],["3","68"],["3","70"],["3","93"],["3","52"],["4","48"],["2","45"],["2","49"],["3","46"],["2","40"],["3","43"],["3","39"],["2","43"],["4","48"],["3","42"],["3","43"],["3","51"],["3","44"],["3","41"],["3","46"],["3","47"],["3","50"],["3","65"],["3","62"],["2","68"],["2","51"]]}
//var donnees = JSON.parse(rawData);
var i, c1 = [], c2 = [], c3 = [], c4 = [], c5 = [], len = rawData.index.length

for (i = 0; i < len; i++) {
    // volume de recherche sur Google, candidat 1
    c1.push(rawData.data[i][0]);
}
for (i = 0; i < len; i++) {
    // volume de recherche sur Google, candidat 2
    c2.push(rawData.data[i][1]);
}

var ctx = document.getElementById("myChart").getContext("2d");
var data = {
    labels: rawData.index,
    datasets: [
        {
            label: rawData.columns[0],
            backgroundColor: "rgba(0,50,220,0.5)",
            borderColor: "rgba(0,50,220,0.8)",
            highlightFill: "rgba(0,50,220,0.75)",
            highlightStroke: "rgba(0,50,220,1)",
            data: c1
        },
        {
            label: rawData.columns[1],
            backgroundColor: "rgba(151,0,0,0.5)",
            borderColor: "rgba(151,0,0,0.8)",
            highlightFill: "rgba(151,0,0,0.75)",
            highlightStroke: "rgba(151,0,0,1)",
            data: c2
        }
    ]
};

var myLineChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        title: {
            display: true,
            text: "Google Trends",
            fontSize: 16
        },
        responsive: true
    }
});