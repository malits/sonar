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
      clear_tracks()
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

  console.log(data.tracks)
  var tracks = []

  for (item of data.tracks) {
    var artist_name = item.artists[0].name
    var img = item.album.images[1]
    var img_src = img.url
    var h = img.height
    var w = img.width
    var track_name = item.name

    var track_text = artist_name + " - " + track_name
    tracks.push({"text": track_text, "src": img_src, "h": h, "w": w})
  }

  return tracks
}

//This is all weird. Refactor probably required?
function show_tracks(tracks) {
  var track_str = ""

  for (t of tracks) {
    insert_image(t.src, t.text)
  }
}

function insert_image(src, text, h, w) {
  var br = document.createElement("br");
  var img = document.createElement("img");
  var track_text = document.createTextNode(text);
  var div = document.createElement("div");

  img.src = src;

  div.appendChild(img);
  div.appendChild(br);
  div.appendChild(track_text);

  document.getElementById("tracks").appendChild(div);
}

function clear_tracks() {
  var tracks = document.getElementById("tracks");
  while (tracks.firstChild) {
      tracks.removeChild(tracks.firstChild);
  }
}
