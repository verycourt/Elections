<!DOCTYPE html>
<html>
	
	<head>
		<title>Parrainages par candidat</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
	</head>

	<body>
		<header><?php include "/var/www/html/site_header.html";?></header>

		<!-- rajouter le body souhaite ici -->
		<div style="margin-left:10%">
		<div class="bar">
			<canvas id="chartParrainages" width="550" height="300"></canvas>
		</div>
		<script src="parrainages.js" type="text/javascript"></script>
		<p> Le nombre de parrainages obtenus est mis à jour périodiquement, aux dates suivantes (indiquées par le dégradé de couleur)  :</p>
		<ul> 
			<li>1er mars</li>
			<li>3 mars</li>
			<li>7 mars (à venir) </li>
			<li>10 mars (à venir)</li>
			<li>14 mars (à venir)</li>
			<li>18 mars (à venir)</li>
		</ul>
		<p><strong> Source des données :</strong> Conseil Constitutionnel. </p>
		</div>
	</body>
</html>
