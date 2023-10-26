function validation() {
    var user = document.getElementById("user").value;
    var pass = document.getElementById("pass").value;

    if (user == "") {
      document.getElementById("username").innerHTML =
        " ** Please fill the email field";
      return false;
    }
    if (pass == "") {
      document.getElementById("passwords").innerHTML =
        " ** Please fill the password field";
      return false;
    }
  }