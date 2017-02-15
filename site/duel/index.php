<!DOCTYPE html>
<html>
	
	<head>
		<title>Réseaux sociaux</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>
		<div>
			<canvas id="myChart" width="700" height="450"></canvas>
		</div>

		<script src="radar.js" type="text/javascript"></script>
	</body>
</html>