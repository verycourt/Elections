<!DOCTYPE html>
<html>

	<head>
		<meta charset="UTF-8"></meta>
		<link rel="stylesheet" href="style.css" />
		<title>Google Trends</title>

	</head>

	<body>
		<h2>Recherches Google sur les principaux thèmes de la campagne présidentielle.</h2>
		<div class="bar">
			<canvas id="myBarChart" width="600" height="450"></canvas>
		</div>

		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.bundle.min.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
		<p> Source des données : Google Trends (www.google.com/trends). </p>
		<script src="js/bar_themes.js" type="text/javascript"></script>
	</body>

</html>
