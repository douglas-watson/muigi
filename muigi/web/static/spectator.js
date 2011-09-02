function getPosition() 
{
    $.ajax({
            method: 'get',
            url: '/_get_position',
            dataType: 'json',
            success: function(data) { 
                $("#position").html(data.position);
                $('#time').html(data.time + " s");
                $('#wait').html(data.wait + " s");
            }
    });
}

function leavePage()
{
    $.post('_quit');
}

$( setInterval(getPosition, 1000) );
$(window).unload(leavePage)
