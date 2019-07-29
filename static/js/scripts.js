$(document).ready( function() {

  var user_msg = "This is a test."

  $("#submit").click( function() {
    send_request(user_msg);
  });
});

function send_request(data) {
  $.ajax({
    url: "test",
    type: "POST",
    dataType: "text",
    contentType: "application/json",
    data: JSON.stringify({"myData": data}),

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
