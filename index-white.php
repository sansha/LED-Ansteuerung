<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>LED Steuerung @ Home</title>
</head>
<body>
Licht an und ausschalten:
<form method="get" action="index-white.php">
<input type="submit" value="Licht ein" name="w_on"> <br>
<input type="submit" value="Licht aus" name="w_off">
</form>
<form action="index-white.php" method="get">
  targetLuminance eingeben: 0 bis 100: 
  <input type="number" name="targetLuminance" min="0" max="100">
  <input type="submit">
</form>
<br>

 <form>
<input type="radio" name="fade" value="0" checked>kein Fade
<br>
<input type="radio" name="fade" value="1" checked>Fade
</form> 


immer erst ausschalten, wenn 'Licht ist an' dasteht und umgekehrt! <br>
nach druecken des Knopfes WARTEN bis die Aktion abgeschlossen ist und das Ergebnis 'Licht ist aus/an' angezeigt wird!
<br> <br>
<?php
if(isset($_GET['w_on'])) {
$val = trim(@shell_exec("./universal.py $fade 1 ")); 
echo "Licht ist an";
}
else if (isset($_GET['w_off'])) {
$val = trim(@shell_exec("./universal.py $fade 0  " ));
echo "Licht ist aus";
}
?>
</body>
</html>