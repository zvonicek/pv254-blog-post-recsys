<?php


function cmd_exec($cmd, &$stdout, &$stderr)
{
    $outfile = tempnam(".", "cmd");
    $errfile = tempnam(".", "cmd");
    $descriptorspec = array(
        0 => array("pipe", "r"),
        1 => array("file", $outfile, "w"),
        2 => array("file", $errfile, "w")
    );
    $proc = proc_open($cmd, $descriptorspec, $pipes);

    if (!is_resource($proc)) return 255;

    fclose($pipes[0]);    //Don't really want to give any input

    $exit = proc_close($proc);
    $stdout = file($outfile);
    $stderr = file($errfile);

    unlink($outfile);
    unlink($errfile);
    return $exit;
}

$user_id = intval($_GET['id']);
$file = __DIR__.DIRECTORY_SEPARATOR."recommender.jar";
cmd_exec("java -jar $file $user_id 10", $results, $error);
//print_r($result);
$json = array();
foreach($results as $result){
    $json[] = intval(str_replace(array("\r", "\n"), '', $result));
}
echo json_encode($json);
//print_r($error);
?>