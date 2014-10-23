function createPlayFunc(cellTag, i, j) {
    return function(e) {
	$.get('/play', {'i': i, 'j': j}, function(data) {
		cellTag.html('X');
		console.log('data: ' + data);
		if (data['status'] === 'done') {
		    $('#winner').html("well the game is over..." + data['winner']);
		} else {
		    var aiPlayTag = $('#cell' + data['x'] + data['y']);
		    aiPlayTag.html('O');
		}
	    });
    };
}

$(function() {
	for (var i in [0,1,2]) {
	    for (var j in [0,1,2]) {
		var cellName = '#cell' + i + j;
		var cellTag = $(cellName);
		var x = i;
		var y = j;

		$(document).on('click', cellName, createPlayFunc(cellTag, i, j));
	    }
	}
    });