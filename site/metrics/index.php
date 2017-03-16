<!DOCTYPE html>
<html>
	
	<head>
		<title>Analyse historique rÃ©seaux sociaux</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
		<link rel="stylesheet" href="style.css" />
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<div class="line">
			<canvas id="m0" width="800" height="500"></canvas>
		</div>
		<div class="line">
			<canvas id="m1" width="800" height="500"></canvas>
		</div>
		<div class="line">
			<canvas id="m2" width="800" height="500"></canvas>
		</div>
		<div class="line">
			<canvas id="m4" width="800" height="500"></canvas>
		</div>
		<div class="line">
			<canvas id="m5" width="800" height="500"></canvas>
		</div>
		<div class="line">
			<canvas id="m6" width="800" height="500"></canvas>
		</div>
		<div class="line">
			<canvas id="m7" width="800" height="500"></canvas>
		</div>

		<script src="metrics_0.js" type="text/javascript"></script>
		<script src="metrics_1.js" type="text/javascript"></script>
		<script src="metrics_2.js" type="text/javascript"></script>
		<script src="metrics_4.js" type="text/javascript"></script>
		<script src="metrics_5.js" type="text/javascript"></script>
		<script src="metrics_6.js" type="text/javascript"></script>
		<script src="metrics_7.js" type="text/javascript"></script>
		
		<p> Les statistiques du buzz sur Facebook représentent le nombre d'utilisateurs qui ont interagi avec la page officielle d'un des candidat.
		Les interactions comprennent notamment les likes, les commentaires ou partages d'une publication de la page du candidat. </p>

		<p> Source des données : Twitter, YouTube et Facebook. </p>
	</body>
</html>