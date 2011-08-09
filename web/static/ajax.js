var SCRIPT_ROOT = '';

// Submit form, and re-render it upon success
$(function() {
    $('input[type="checkbox"]').live('click', function() {
        $.post('/_set_states',
			$('#control_form').serialize(),
			function(data) {
				$('div#controls').html(data.html_form);
				// Fade in the response box, for effect:
				$('#response').hide().fadeIn(1000);
				$('#submit').hide();
			}),
			'json'
		});
	return false;
});

$(function() {
	$('#submit').hide();
});
