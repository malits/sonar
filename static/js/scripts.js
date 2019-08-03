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
      console.log("Finished attempting POST request...")
    },

    success: function(res) {
      console.log(res)
      $("#test_span").text(res.prob)
    },

    error: function() {
      console.log("Error in POST request")
    },
  });
}
