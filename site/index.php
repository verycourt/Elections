<!DOCTYPE html>
<html>

	<head>
		<title>Predict The President</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<link rel="manifest" href="manifest.json">
	</head>

	<body>
		<header><?php include "/var/www/html/site_header.html";?></header>

		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Pollster</h2></div>
			<div class="panel panel-body wrapper" style="text-align:center">
				<link rel="stylesheet" type="text/css" href="1ertour/Pollster_1T_V0.css">
				<div id="dashboard-pollster">
					<button  id="button" class="btn-danger btn-responsive" style="text-align:center;padding-bottom:0.2%;
					font-size:0.9vw;width:10%;max-height:7%;position:relative;left:35%;bottom:25%;">Tout sélectionner</button>
					<script src="https://d3js.org/d3.v3.min.js"></script>
					<script src="1ertour/Pollster_1T_V0.js"></script>
				</div>
			</div>
		</div>

		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center"><h2>Veille réseaux sociaux</h2></div>
			<div class="col-md-16 panel panel-body" style="margin-left:25%">
				<div>
					<canvas id="radar" width="700" height="450"></canvas>
				</div>

				<script src="/radar/radar.js" type="text/javascript"></script>
				<p>* Les likes des vidéos YouTube sont une moyenne sur les 10 dernières vidéos publiées sur la chaîne des candidats.</p>
				<p>** Les mentions sur Facebook représentent le nombre d'utilisateurs qui ont interagi avec la page officielle d'un des candidat. Les interactions comprennent notamment les likes, les commentaires ou partages d'une publication de la page du candidat.</p>
				<p><strong>Sources :</strong> Facebook, Twitter, Youtube. Données actualisées tous les jours. </p>
			</div>
		</div>

		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center"><h2>Sondages du second tour :<br> Hypothèse <em>Marine Le Pen</em> VS <em>Emmanuel Macron</em></h2></div>
			<div class="col-md-16 panel panel-body" id="dashboard">
				<script src="2ndtour/graphes.js"> </script>
				<script>afficher("2ndtour/mlpVSem.tsv")</script>
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
			<div class="panel panel-heading text-center"><h2>Mots associés aux candidats sur Twitter</div>
			<div class="panel panel-body" style="text-align:center">
				<p><strong>Méthodologie :</strong> Nuages de mots-clés rafraîchis tous les jours à 14h sur les 200 000 derniers tweets portant sur les candidats</p>
				<br><br><br>
				<h4>François Fillon</h4><img width="30%" height="25%" src="decompte/cloud_fillon.png">
				<br><br><br>
                              	<h4>Benoît Hamon</h4><img width="30%" height="25%" src="decompte/cloud_hamon.png">
				<br><br><br>
                                <h4>Jean-Luc Mélenchon</h4><img width="30%" height="25%" src="decompte/cloud_mélenchon.png">
				<br><br><br>
                                <h4>Marine Le Pen</h4><img width="30%" height="25%" src="decompte/cloud_lepen.png">
				<br><br><br>
                                <h4>Emmanuel Macron<h4><img width="30%" height="25%" src="decompte/cloud_macron.png">
			</div>
		</div>
	</body>
</html>
