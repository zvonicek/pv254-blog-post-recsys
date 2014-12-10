<?php

date_default_timezone_set('Europe/Prague');
ini_set('memory_limit', '2048M');

function println($s)
{
	echo date("[H:i:s] ") . $s . "\n";
}

println("Starting.");

$i = 0;
$users = [];
$blogs = [];
$map = [];

$handle = fopen("untransformed.csv", "r");
while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
	list($userId, $blogId, $rate) = $data;

	$users[$userId][$blogId] = $rate;

	$blogs[$blogId] = TRUE;
	if (!isset($map[$userId])) {
		$map[$userId] = $i++;
	}

	if ($i === 100) {
		//break;
	}
}
fclose($handle);

$blogs = array_keys($blogs);
$usersCount = count($users);
$blogsCount = count($blogs);
println("User count: " . $usersCount . ".");
println("Blogs count: " . $blogsCount . ".");

println("Creating empty vectors.");

$ratings = [];

foreach ($blogs as $blogId) {
	$ratings[$blogId] = array_fill(0, $usersCount, 0);
}


println("Filling users.");

foreach ($users as $userId => $userRatings) {
	foreach ($userRatings as $blogId => $userRating) {
		$ratings[$blogId][$map[$userId]] = $userRating;
	}
}


println("Calculating pows.");

$pows = [];
foreach ($blogs as $blogId) {
	$sum = 0;
	for ($i = 0; $i < $usersCount; $i += 1) {
		$sum += pow($ratings[$blogId][$i], 2);
	}
	$pows[$blogId] = sqrt($sum);
}


println("Calculating similarities.");

$todoBlogs = $blogs;

$similarities = [];
foreach ($todoBlogs as $blogId_a) {
	foreach ($blogs as $blogId_b) {
		if (isset($similarities[$blogId_b][$blogId_a])) {
			continue;
		}

		$product = 0;
		for ($i = 0; $i < $usersCount; $i += 1) {
			$product += $ratings[$blogId_a][$i] * $ratings[$blogId_b][$i];
		}

		$divider = $pows[$blogId_a] * $pows[$blogId_b];
		if ($divider == 0) {
			$similarities[$blogId_a][$blogId_b] = 0;
		} else {
			$similarities[$blogId_a][$blogId_b] = $product / $divider;
		}
	}
	println("- Similarity done for: " . $blogId_a);
}


foreach ($todoBlogs as $blogId) {
	$data = $similarities[$blogId];
	arsort($data);
	$i = 0;
	foreach ($data as $sblogId => $rating) {
		println("-- blogId: " . $blogId . " - similar blogId: " . $sblogId . "  - rating: " . $rating);
		$i++;
		if ($i == 10) {
			break;
		}
	}
}
