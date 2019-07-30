$(document).ready( function() {

  var user_msg = {"message": "Today was so bad!"}

  $("#submit").click( function() {
    predict(user_msg);
  });
});

function predict(data) {
  $.ajax({
    url: "predict",
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
