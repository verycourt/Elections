<!DOCTYPE html>
<html>
	
	<head>
		<title>Titre ici</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>
		<div>
			<canvas id="myChart" width="350" height="200"></canvas>
		</div>

		<script src="radar.js" type="text/javascript"></script>
	</body>
</html>