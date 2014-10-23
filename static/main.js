function createPlayFunc(cellTag, i, j) {
    return function(e) {
	$.get('/play', {'i': i, 'j': j}, function(data) {
		console.log('data: ' + data);
		cellTag.html('X');
		if (data['winner'] === 'done') {
		    console.log("well somebody won");
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

		console.log('cellTag: ' + cellName);
		$(document).on('click', cellName, createPlayFunc(cellTag, i, j));
	    }
	}
    });