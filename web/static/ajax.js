var SCRIPT_ROOT = '';

$(function() {
    $("#ajaxsubmit").live('click', function() {
        $.post('/_set_states',
			$('#control_form').serialize(),
			function(data) {
				$('div#controls').html(data.html_form).fadeIn(1000);
			}),
			'json'
		});
	return false;
});

function whatevs() {
		$("#ajaxsubmit").html("Hello World");
};

