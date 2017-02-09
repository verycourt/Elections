<!DOCTYPE html>
<html>

	<head>
		<meta charset="UTF-8"></meta>
		<link rel="stylesheet" href="style.css" />
		<title>Google Trends</title>
	</head>

	<body>
		<div class="line">
			<canvas id="myChart" width="350" height="200"></canvas>
		</div>
		<div class="bar">
			<canvas id="myBarChart" width="150" height="200"></canvas>
		</div>

		<p> Source des données : Google Trends (www.google.com/trends). </p>
		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.bundle.min.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.17.1/locale/fr.js"></script>
		
		<script src="js/candidats_A.js" type="text/javascript"></script>
	</body>

</html>
