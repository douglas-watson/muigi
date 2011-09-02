function sendHeartbeat() {
    /* Used to make sure the player is still online */
    $.ajax({
            method: 'get',
            url: '/_player_heartbeat',
            dataType: 'text',
            success: function(data) {
                setTimeout(sendHeartbeat, 500);
                // TODO if status is no longer player, switch to spectator mode
            }
    });
}

function getPosition() 
{
    /* Gets the position in line of a spectator, and doubles as a heartbeat.
     * If the status switches from 'spectator' to 'player', load the controls
     * form and start the player heartbeats. */
    $.ajax({
            method: 'get',
            url: '/_get_position',
            dataType: 'json',
            success: function(data) { 
                console.log(data.status);
                if ( data.status == "spectator" ) {
                    // Update status information
                    $('#status').html("Please wait for your turn.");
                    $("#position").html(data.position);
                    $('#wait').html(data.wait + " s");
                    // And schedule a new poll in a second
                    setTimeout(getPosition, 1000);
                } else if ( data.status == "player" ) {
                    // Render the form
                    $('#controls').html(data.form);
                    setTimeout(sendHeartbeat, 500);
                }
            }
    });
}

function leavePage()
{
    $.post('_quit');
}

$( setTimeout(getPosition, 1000) );
$(window).unload(leavePage)
