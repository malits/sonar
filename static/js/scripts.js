$(document).ready( function() {

  $("#submit").click( function() {

    var input_msg = $("#msg_input").val()
    var user_msg = {"message": input_msg}

    predict(user_msg);
  });
});

function predict(data) {
  $.ajax({
    url: "predict",
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    data: JSON.stringify(data),

    complete: function() {
      console.log("Finished attempting POST request")
    },

    success: function(res) {
      console.log(res.prob)
      tracks = assemble_tracks(res.recs)
      show_tracks(tracks)
    },

    error: function() {
      console.log("Error in POST request")
    },
  });
}

function assemble_tracks(data) {
  //console.log(JSON.parse(data))
  //var parsed_data = JSON.parse(data)
  console.log(data)

  var tracks = []

  for (item of data.tracks) {
    var artist_name = item.artists[0].name
    var track_name = item.name

    var track_text = artist_name + " - " + track_name
    tracks.push(track_text)
  }

  return tracks
}

//This is all weird. Refactor probably required?
function show_tracks(tracks) {
  var track_str = ""

  for (t of tracks) {
    track_str = track_str + "\n" + t
  }

  $("#test_span").text(track_str)
}
