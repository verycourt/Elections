<!DOCTYPE html>
<html>

	<head>
		<title>DataPrez Le Point</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Pollster</h2></div>
			<div class="panel panel-body wrapper" style="text-align:center">
			<link rel="stylesheet" type="text/css" href="1er tour/Pollster_1T_V0.css">
			<div id="dashboard-pollster">
			<script src="https://d3js.org/d3.v3.min.js"></script>
			<script src="1er tour/Pollster_1T_V0.js"></script>
			<button  id="button" class="btn-success btn-responsive" style="text-align:center;padding-bottom:0.2%; 
			font-size:0.7vw;width:10%;max-height:7%;position:absolute;right:27%;top:15px;">Tout sélectionner</button>
			</div>				
			</div>
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading" style="text-align:center;">
				<h2 class="text-center"> Second tour : hypothèse Marine Le Pen VS Emmanuel Macron</h2></div>
				<div class="col-md-16 panel panel-body" id="dashboard" style="text-align:left;">
				<script src="2nd tour/graphes.js"> </script>
				<script>afficher("2nd tour/mlpVSem.tsv")</script>
				</div>
			</div>
                </div>
		<div class="line">
			<canvas id="myChart" width="350" height="200"></canvas>
		</div>
		<div class="bar">
			<canvas id="myBarChart" width="150" height="200"></canvas>
		</div>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.bundle.min.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
		<p> Source des données : Google Trends (www.google.com/trends). </p>
		<script src="gtrends/js/candidats_A.js" type="text/javascript"></script>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>WordCloud Twitter par candidat sur 3 jours</h2></div>
			<div class="panel panel-body" style="text-align:center">
				<h2>WordCloud Benoît Hamon</h2>
				<img width="50%" height="50%" src="decompte/hamon_cloud.png">
			</div>
		</div>
	</body>
</html>
