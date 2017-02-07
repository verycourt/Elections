<!DOCTYPE html>
<html>

	<head>
		<title>DataPrez Le Point</title>
		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/site_style.css";?></style>
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Pollster</h2></div>
			<div class="panel panel-body" style="text-align:left">
				<iframe src="1er tour/Pollster_1T_V0.html" scrolling="no" frameborder="no" marginwidth="0" width="1200" align="center" height="550"></iframe>
			</div>
		</div>

		<div class="col-md-16 panel panel-default">
			<div class="panel panel-heading text-center"><h2>Google Trends</h2></div>
			<div class="panel panel-body" style="text-align:center">
				<iframe src="/gtrends/gtrends.html" scrolling="no" frameborder="no" marginwidth="0" width="960" align="center" height="800"></iframe>
			</div>
		</div>

	</body>
</html>