function switchView(view)
{
	$("div#dynamic").load(view)
}

var obj;
function getCategory()
{
	obj = $.get('/debug/', function(data)
	{
		console.log(data);
	});
}

var BAD_ROOM_CODE = 1;