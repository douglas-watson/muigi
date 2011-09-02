var SCRIPT_ROOT = '';

function submitForm() {
    $.post('/_set_states',
            $('#control_form').serialize(),
            function(data) {
            $('div#controls').html(data.html_form);
            // Fade in the response box, for effect:
            $('#response').hide().fadeIn(1000);
            $('#submit').hide();
            }),
        'json'
}

// Submit form, and re-render it upon success
$(function() {
    $('input[type="checkbox"]').live('click', submitForm);
	return false;
});

$(function() {
	$('#submit').hide();
});
