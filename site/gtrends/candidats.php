<!DOCTYPE html>
<html>
	
	<head>
		<title>Live Google Trends</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
		<link rel="stylesheet" href="style.css" />
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<!-- rajouter le body souhaite ici -->
		<div class="line">
			<canvas id="myChart" width="900" height="500"></canvas>
		</div>
		<div class="bar">
			<canvas id="myBarChart" width="250" height="300"></canvas>
		</div>
		<script src="js/candidats_A.js" type="text/javascript"></script>
		<p> Source des données : Google Trends (www.google.com/trends). </p>
	</body>
</html>