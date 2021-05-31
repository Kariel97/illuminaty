<?php
header('Content-Type: text/html');
{
  $lat = $_POST['Lat'];
  $lon = $_POST['Lon'];
 
  $coordinates = "https://www.google.com/maps/place/" . $lat . "+" . $lon;

  $f = fopen('geo.txt', 'w+');
  fwrite($f, $coordinates);
  fclose($f);
}
?>