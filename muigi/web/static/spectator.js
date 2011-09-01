function getPosition() 
{
    $.ajax({
            method: 'get',
            url: '/_get_position',
            dataType: 'json',
            success: function(data) { 
                $("#position").html(data.position);
                $('#time').html(data.time + " s");
            }
    });
}

$( setInterval(getPosition, 1000) );
