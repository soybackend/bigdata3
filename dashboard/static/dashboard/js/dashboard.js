$(document).ready(function(){

	'use strict';

	// Tooltip for flot chart
	function showTooltip(x, y, contents) {
		$('<div id="tooltip" class="tooltipflot">' + contents + '</div>').css( {
			position: 'absolute',
			display: 'none',
			top: y + 5,
			left: x + 5
		}).appendTo('body').fadeIn(200);
	}

	// Knob
	$('.dial-success').knob({
		readOnly: true,
		width: '70px',
		bgColor: '#E7E9EE',
		fgColor: '#259CAB',
		inputColor: '#262B36'
	});

	$('.dial-danger').knob({
		readOnly: true,
		width: '70px',
		bgColor: '#E7E9EE',
		fgColor: '#D9534F',
		inputColor: '#262B36'
	});

	$('.dial-info').knob({
		readOnly: true,
		width: '70px',
		bgColor: '#66BAC4',
		fgColor: '#fff',
		inputColor: '#fff'
	});

	$('.dial-warning').knob({
		readOnly: true,
		width: '70px',
		bgColor: '#E48684',
		fgColor: '#fff',
		inputColor: '#fff'
	});


});
