<?php

error_reporting(E_ALL);

//RGB-PI-server's address
$service_port = 4321;
$address = "127.0.0.1";

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
$result = socket_connect($socket, $address, $service_port);

//$cmd = "fade 2 {x:000000}";
$cmd = $_GET["cmd"];

socket_write($socket, $cmd, strlen($cmd));
socket_close($socket);

?>