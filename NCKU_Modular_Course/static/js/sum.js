$(document).ready(function () {
  $("#btn_calculateSum").click(function () {
    const num1 = parseFloat(document.getElementById("num1").value);
    const num2 = parseFloat(document.getElementById("num2").value);

    if (isNaN(num1) || isNaN(num2)) {
      document.getElementById("result").innerText =
        "Please enter a valid number!";
      return;
    }

    const formData = {};

    formData["num1"] = num1;
    formData["num2"] = num2;

    $.ajax({
      url: "/ajax_sum/",
      method: "GET",
      data: formData,
      success: function (response) {
        sum = response["sum"];
        document.getElementById("result").innerText = `sum: ${sum}`;
      },
      error: function (error) {
        console.log("Error: ", error);
      },
    });
  });
});
