var SCRIPT_ROOT = '';

// Submit form, and re-render it upon success
$(function() {
    $("#ajaxsubmit").live('click', function() {
        $.post('/_set_states',
			$('#control_form').serialize(),
			function(data) {
				$('div#controls').html(data.html_form).fadeIn(1000);
			}),
			'json'
		});
	// return false;
});
