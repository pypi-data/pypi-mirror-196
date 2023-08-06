<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript" src="./MekongJS.js"></script>
</head>
<body>
    Hello World
    </br>
    <button class="submit" onclick="submit()">Test Task</button>

    <script>
    function submit(){
        var params = '{"fn_name":"test","param":{"text":"Hello World"}}'
        MekongJS.excuting(params, function(res) {});
    }
    </script>
</body>
</html>