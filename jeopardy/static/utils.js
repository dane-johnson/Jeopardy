function switchView(view)
{
	$("div#dynamic").load(view)
}

function getCategory(game)
{
	if(! ('categories' in game))
	{
		game.categories = [];
	}
	$.get('/category/', function(data)
	{
		game.categories.push(JSON.parse(data));
	});
}

var BAD_ROOM_CODE = 1;