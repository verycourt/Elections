<!DOCTYPE html>
<html>

	<head>
		<title>DataPrez Le Point</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Pollster</h2></div>
			<div class="panel panel-body wrapper" style="text-align:center">
				<iframe src="1er tour/Pollster_1T_V0.html" scrolling="no" frameborder="no" ></iframe>
			</div>
		</div>
                <div class="col-md-16 panel panel-default">
                        <div class="panel panel-heading text-center"><h2>Pollster 2nd Tour</h2></div>
                        <div class="panel panel-body">
                                <iframe src="2nd tour/testemvsmlp.html" frameborder="no" scrolling ="no" width="1600" align="center" height="500"></iframe>
                        </div>
                </div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Google Trends</h2></div>
			<div class="panel panel-body" style="text-align:center">
				<iframe src="/gtrends/candidats.php" frameborder="no" scrolling ="no" width="1000" align="center" height="850"></iframe>
			</div>
                </div>
		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>WordCloud Twitter par candidat sur 3 jours</h2></div>
			<div class="panel panel-body" style="text-align:center">
				<h2>WordCloud Benoît Hamon</h2>
				<img width="50%" height="50%" src="decompte/hamon_cloud.png">
			</div>
		</div>
	</body>
</html>
