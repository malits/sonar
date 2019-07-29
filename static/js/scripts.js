$(document).ready( function() {

  var user_msg = {"message": "Today was so bad!"}

  $("#submit").click( function() {
    send_post_request(user_msg);
  });

  $("#retrieve").click(function() {
    send_get_request();
  });
});

function send_post_request(data) {
  $.ajax({
    url: "test",
    type: "POST",
    dataType: "text",
    contentType: "application/json",
    data: JSON.stringify(data),

    complete: function() {
      console.log("Finished attempting POST request...")
    },

    success: function() {
      console.log("Successful POST request!")
    },

    error: function() {
      console.log("Error in POST request")
    },
  });
}

function send_get_request() {
  $.ajax({
    url: "test",
    dataType: "json",

    complete: function() {
      console.log("Finished attempting GET request...")
    },

    success: function() {
      console.log("Successful GET request!")
    },

    error: function() {
      console.log("Error in GET request")
    },
  }).done(function (res) {
    $('#test_span').text(res.score);
  });
}
