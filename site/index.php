<!DOCTYPE html>
<html>

	<head>
		<title>DataPrez</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<link rel="manifest" href="manifest.json">
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h5>Pollster</h5></div>
			<div class="panel panel-body wrapper" style="text-align:center">
				<link rel="stylesheet" type="text/css" href="1er tour/Pollster_1T_V0.css">
				<div id="dashboard-pollster">
					<button  id="button" class="btn-danger btn-responsive" style="text-align:center;padding-bottom:0.2%; 
					font-size:0.7vw;width:10%;max-height:7%;position:relative;left:35%;bottom:25%;">Tout sélectionner</button>
					<script src="https://d3js.org/d3.v3.min.js"></script>
					<script src="1er tour/Pollster_1T_V0.js"></script>
				</div>				
			</div>
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center">
				<h5> Second tour : hypothèse Marine Le Pen VS Emmanuel Macron</h5></div>
				<div class="col-md-16 panel panel-body" id="dashboard">
				<script src="2nd tour/graphes.js"> </script>
				<script>afficher("2nd tour/mlpVSem.tsv")</script>
				</div>
			</div>
                </div>
	
		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center">
			<h5> Suivi des recherches google par candidat</h5></div>
			<div class="col-md-16 panel panel-body">
				<div class="line">
					<canvas id="myChart" width=900 height=500></canvas>
				</div>
				<div class="bar" style="text-align:center;">
					<canvas id="myBarChart" width=250 height=300></canvas>
				</div>
				<script src="gtrends/js/candidats_A.js" type="text/javascript"></script>
			</div>
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h5>Décompte de mentions Twitter par candidats sur 3 jours glissants</h5></div>
			<div id="twittermentions" class="panel panel-body">
				<script src="decompte/histo_count.js"> </script>
				<link rel="stylesheet" href="decompte/styledecompte.css">
			</div>
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h5>WordCloud Twitter par candidat sur 3 jours</h5></div>
			<div class="panel panel-body" style="text-align:center">
				<img width="80%" height="80%" src="decompte/hamon_cloud.png">
			</div>
		</div>
	</body>
</html>
