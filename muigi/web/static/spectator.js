// TODO: implement timeouts consistant with the server timeout, and return an
// error message in consequence (i.e, after 10 seconds of no server response,
// say 'appears you've lost your connection to the server. Sucks for you.'
function playerHeartbeat() {
    /* Used to make sure the player is still online */
    $.ajax({
            method: 'get',
            url: '/_player_heartbeat',
            dataType: 'json',
            success: function(data) {
                if ( data.status == 'player' ) {
                    $("#time").html(data.remaining_time + " s");
                    setTimeout(playerHeartbeat, 500);
                } else if ( data.status == 'spectator' ) {
                    // player has been deleted from queue. Redirect to
                    // /spectator to start all over again.
                    window.location = "/";
                }
            }
    });
}

function spectatorHeartbeat() 
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
                    setTimeout(spectatorHeartbeat, 1000);
                } else if ( data.status == "player" ) {
                    // Render the form
                    $('#controls').html(data.form);
                    setTimeout(playerHeartbeat, 500);
                }
            }
    });
}

function leavePage()
{
    /* Called when the users navigates away from the page. On the server side,
     * deletes the user from the waiting line. */
    $.post('_quit');
}

function submitForm() {
    $.ajax({
            method: 'post',
            url: '/_set_states',
            datatype: 'json',
            data: $('#control_form').serialize(),
            success: function(data) {
                $('div#controls').html(data.html_form);
                // Fade in the response box, for effect:
                $('#response').hide().fadeIn(1000);
            }
        });
}
// Submit form, and re-render it upon success
$(function() {
    $('input[type="checkbox"]').live('click', submitForm);
	return false;
});

$( setTimeout(spectatorHeartbeat, 1000) );
$(window).unload(leavePage)
