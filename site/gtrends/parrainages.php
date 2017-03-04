<!DOCTYPE html>
<html>
	
	<head>
		<title>Parrainages</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
		<link rel="stylesheet" href="style.css" />
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<!-- rajouter le body souhaite ici -->

		<div class="bar">
			<canvas id="chartParrainages" width="650" height="400"></canvas>
		</div>
		<script src="parrainages.js" type="text/javascript"></script>
		<p> Source des données : conseil constitutionnel. </p>
	</body>
</html>