<!DOCTYPE html>
<html>
	
	<head>
		<title>Google Trends</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/site_style.css";?></style>
		<link rel="stylesheet" href="style.css" />
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<div class="line">
			<canvas id="myChart" width="350" height="200"></canvas>
		</div>
		<div class="bar">
			<canvas id="myBarChart" width="150" height="200"></canvas>
		</div>

		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.bundle.min.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
		<p> Source des données : Google Trends (www.google.com/trends). </p>
		<script src="js/linechart_5candidats.js" type="text/javascript"></script>

	</body>
</html>