<!DOCTYPE html>
<html>
	
	<head>
		<title>Valls vs. Le Pen</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center">
				<h2>Hypothèse Marine Le Pen VS Manuel Valls</h2>
				<script src="graphes.js"> </script>
				<script>afficher("mlpVSmv.tsv")</script>
			</div>
		</div>
		<div class="col-md-16 panel panel-body" id="dashboard" style="text-align:center"></div>
	</body>
</html>
