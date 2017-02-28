<!DOCTYPE html>
<html>

	<head>
		<title>Fillon vs. Le Pen</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
		<script src="http://d3js.org/d3.v3.min.js"></script>

	</head>

	<body>
		<header><?php include "/var/www/html/site_header.html";?></header>

		<div class="col-md-16 panel panel-default">
			<div class="col-md-16 panel-heading text-center">
				<h2>Hypothèse Marine Le Pen VS François Fillon</h2>
				<script src="graphes.js"> </script>
				<script>afficher("mlpVSff.tsv")</script>
			</div>
		</div>
		<div class="col-md-16 panel panel-body" id="dashboard" style="text-align:center"></div>
	</body>
</html>
