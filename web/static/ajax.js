var SCRIPT_ROOT = '';

$(function() {
    $("#ajaxsubmit").bind('click', function() {
        $.post('/_set_states', 
            { a_state: $('input[name="a_state"]').val(),
			  b_state: $('input[name="b_state"]').val() 
		    }, function(data) {
                $('span#response').html(data.feedback).fadeIn(1000);
				$('input[name="a_state"]').val(data.new_a);
				$('input[name="b_state"]').val(data.new_b);
            })
	});
	return false;
});

function whatevs() {
		$("#ajaxsubmit").html("Hello World");
};

