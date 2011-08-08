jQuery(document).ready(function() {
    jQuery("#submit").click(function() {
        var input_string = $("#colour").val();
        jQuery.ajax({
            type: "POST",
            data: {colour : input_string},
            success: function(data) {
                jQuery('span#response').html(data).hide().fadeIn(1500);
            },
        });
        return false;
    });
});



