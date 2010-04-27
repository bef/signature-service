<?php

function error($code) {
	header('HTTP/1.0 500 $code boo.');
	die($code);
}

function cmd($s, $cmd)
{
	socket_write($s, $cmd . "\n");
	return read_reply($s);
}

function read_reply($s)
{
	$str = socket_read($s, 10000, PHP_NORMAL_READ); // read up to \n
	if (preg_match('/^200 READ=(\d+)/', $str, $matches)) // multiline read?
		return socket_read($s, $matches[1], PHP_BINARY_READ);
	if (preg_match('/^200 (.*)$/', $str, $matches)) // normal 200
		return $matches[1];
	error(504); // error condition
}

// limit actions
if (!isset($_REQUEST['action']) || !in_array($_REQUEST['action'], array('sign', 'key'), true))
	error(501);

// limit message - alphabet and size
if ($_REQUEST['action'] == 'sign' && (!isset($_REQUEST['msg']) || strlen($_REQUEST['msg']) > 255 || preg_match('/[^a-zA-Z0-9;:_ -]/', $_REQEST['msg']) ))
	error(502);

// open socket to sis server
$s = socket_create(AF_UNIX, SOCK_STREAM, 0);
if (!socket_connect($s, "/tmp/sis.sock"))
	error(503);

// perform action
switch($_REQUEST['action']) {
	case "sign":
		$result = cmd($s, "SIGN " . $_REQUEST['msg']);
		header("Content-Type: text/plain");
		echo $result;
		break;
	case "key":
		$result = cmd($s, "EXPORTKEY");
		header("Content-Type: text/plain");
		echo $result;
		break;
}


// close socket
socket_close($s);
