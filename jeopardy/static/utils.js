function switchView(view)
{
	$("div#dynamic").load(view)
}

function getCategory(board)
{
	if(! ('categories' in board))
	{
		board.categories = [];
	}
	$.get('/category.json?room_code='+room_code, function(data)
	{
		board.categories.push(JSON.parse(data));
		board.onLoad();
	});
}

function Board()
{
	this.onLoad = null;
	this.categories = [];
}
var BAD_ROOM_CODE = 1;