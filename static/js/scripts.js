$(document).ready( function() {

  var user_msg = {"message": "This is a test."}

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
      console.log("finished")
    },

    success: function() {
      console.log("Success!")
    },

    error: function() {
      console.log("error")
    },
  });
}

function send_get_request() {
  $.ajax({
    url: "test",
    dataType: "json",

    complete: function() {
      console.log("Done")
    },

    success: function() {
      console.log("success")
    },

    error: function() {
      console.log("error")
    },
  }).done(function (test) {
    $('#test_span').text(test.test);
  });
}
