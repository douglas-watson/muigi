function sendHeartbeat() {
    /* Used to make sure the player is still online */
    $.ajax({
            method: 'get',
            url: '/_player_heartbeat',
            dataType: 'json',
            success: function(data) {
                if ( data.status == 'player' ) {
                    $("#time").html(data.remaining_time + " s");
                    setTimeout(sendHeartbeat, 500);
                } else if ( data.status == 'spectator' ) {
                    // player has been deleted from queue. Redirect to
                    // /spectator to start all over again.
                    window.location = "/spectator";
                }
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
            url: '/_spectator_heartbeat',
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
