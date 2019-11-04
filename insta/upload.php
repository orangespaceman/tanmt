<?php

set_time_limit(60);
date_default_timezone_set('UTC');

require "vendor/autoload.php";
require "uploader/uploader.php";

$imagePath = $argv[1];
$title = $argv[2];
$tags = $argv[3];
$username = $argv[4];
$password = $argv[5];

$uploader = new Uploader();
$uploader->upload($imagePath, $title, $tags, $username, $password);
