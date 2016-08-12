function switchView(view)
{
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function()
	{
		if(xhr.status == 200)
		{
			$("div#dynamic").html(xhr.responseText);
		}
	};
	xhr.open("GET", view);
	xhr.send();
}
