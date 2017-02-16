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
			<div class="panel panel-heading text-center"><h2>Pollster</h2></div>
			<div class="panel panel-body wrapper" style="text-align:center">
				<link rel="stylesheet" type="text/css" href="1er tour/Pollster_1T_V0.css">
				<div id="dashboard-pollster">
					<button  id="button" class="btn-danger btn-responsive" style="text-align:center;padding-bottom:0.2%; 
					font-size:0.9vw;width:10%;max-height:7%;position:relative;left:35%;bottom:25%;">Tout sélectionner</button>
					<script src="https://d3js.org/d3.v3.min.js"></script>
					<script src="1er tour/Pollster_1T_V0.js"></script>
				</div>				
			</div>
		</div>

		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center"><h2>Veille réseaux sociaux</h2></div>
			<div class="col-md-16 panel panel-body">
				<div>
					<canvas id="radar" width="700" height="450"></canvas>
				</div>

				<script src="/duel/radar.js" type="text/javascript"></script>
				<p> Sources : Facebook, Twitter, Youtube. Données actualisées tous les jours. </p>
			</div>
		</div>

		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center"><h2>Second tour : hypothèse Marine Le Pen VS Emmanuel Macron</h2></div>
			<div class="col-md-16 panel panel-body" id="dashboard">
				<script src="2nd tour/graphes.js"> </script>
				<script>afficher("2nd tour/mlpVSem.tsv")</script>
			</div>
		</div>
	
		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center"><h2>Evolution des recherches Google par candidat sur 24h</h2></div>
			<div class="col-md-16 panel panel-body">
				<div class="line">
					<canvas id="myChart" width=900 height=500></canvas>
				</div>
				<div class="bar" style="text-align:center;">
					<canvas id="myBarChart" width=250 height=300></canvas>
				</div>
				<script src="gtrends/js/trends_24h.js" type="text/javascript"></script>
			</div>
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Décompte de mentions Twitter par candidats sur 3 jours glissants</h2></div>
			<div id="twittermentions" class="panel panel-body">
				<script src="decompte/histo_count.js"> </script>
				<link rel="stylesheet" href="decompte/styledecompte.css">
			</div>
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Décompte de mentions Twitter sur 1 journée</h2></div>
			<iframe src="http://34.193.36.41/decompte/indexdays.html" width="100%" height="100%">
  				<p>Your browser does not support iframes.</p>
			</iframe>			
		</div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Analyse sémantique automatique sur Twitter</div>
			<div class="panel panel-body" style="text-align:center">
				<img width="30%" height="25%" src="decompte/topics/twitter_topic0.png">
                                <img width="30%" height="25%" src="decompte/topics/twitter_topic1.png">
                                <img width="30%" height="25%" src="decompte/topics/twitter_topic2.png">
                                <img width="30%" height="25%" src="decompte/topics/twitter_topic3.png">
                                <img width="30%" height="25%" src="decompte/topics/twitter_topic4.png">
                                <img width="30%" height="25%" src="decompte/topics/twitter_topic5.png">
				<p class="text center">Détection automatique des clusters de mots les plus associés dans les 200 000 derniers tweets récupérés : un nuage par cluster</p>
			</div>
		</div>
	</body>
</html>
