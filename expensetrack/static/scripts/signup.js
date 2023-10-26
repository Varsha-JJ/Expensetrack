function validation() {
  var user = document.getElementById("fname").value;
  var user2 = document.getElementById("user").value;
  var user1 = document.getElementById("lname").value;
  var pass = document.getElementById("pass").value;
  var emails = document.getElementById("emails").value;
  var confirmpass = document.getElementById("conpass").value;

  if (user == "") {
     document.getElementById("ufname").innerHTML =
      " ** Please fill the firstname field";
    return false;
  }
  if (user.length <= 2 || user.length > 20) {
    document.getElementById("ufname").innerHTML =
      " ** Firstname lenght must be between 2 and 20";
    return false;
  }
  if (!isNaN(user)) {
    document.getElementById("ufname").innerHTML =
      " ** only characters are allowed";
    return false;
  }

  if (user1 == "") {
    b = document.getElementById("ulname").innerHTML =
      " ** Please fill the last name field";
      console.log(b);
    return false;
  }
  if (user1.length == 0) {
    document.getElementById("ulname").innerHTML =
      " ** Last name must be filled";
    return false;
  }
  if (!isNaN(user1)) {
    document.getElementById("ulname").innerHTML =
      " ** only characters are allowed";
    return false;
  }


  
  if (emails == "") {
    document.getElementById("emailids").innerHTML =
      " ** Please fill the email id field";
    return false;
  }
  if (emails.indexOf("@") <= 0) {
    document.getElementById("emailids").innerHTML = " ** Invalid Email";
    return false;
  }

  if (
    emails.charAt(emails.length - 4) != "." &&
    emails.charAt(emails.length - 3) != "."
  ) {
    document.getElementById("emailids").innerHTML = " ** Invalid Email";
    return false;
  }


  if (user2 == "") {
    document.getElementById("username").innerHTML =
      " ** Please fill the username field";
    return false;
  }
  if (user2.length <=2 ) {
    document.getElementById("username").innerHTML =
      " ** Username lenght must include more characters";
    return false;
  }
  if (!isNaN(user2)) {
    document.getElementById("username").innerHTML =
      " ** only characters are allowed";
    return false;
  }






  if (pass == "") {
    document.getElementById("passwords").innerHTML =
      " ** Please fill the password field";
    return false;
  }
  // if (pass.length <= 7 ) {
  //   document.getElementById("passwords").innerHTML =
  //     " ** Passwords lenght must be between  8 and 20";
  //   return false;
  // }

  if (!pass.match(/(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8}/)) {
        document.getElementById("passwords").innerHTML =
          " ** Passwords contain min 8 chars with at least 1 uppercase ,number and 1 special character";
        return false;
      }


  if (confirmpass == "") {
    document.getElementById("confrmpass").innerHTML =
      " ** Please fill the password field";
    return false;
  }
  if (pass != confirmpass) {
    document.getElementById("confrmpass").innerHTML =
      " ** Password does not match the confirm password";
    return false;
  }


}


// onkeyup validation


function fnameValidation(inputTxt){
    
  var regx = /^[a-zA-Z\s, ]+$/;
  var textField = document.getElementById("fname");
  var span = document.getElementById("ufname");
      
  if(inputTxt.value != '' ){
  
      if(inputTxt.value.length >= 3){
      
          if(inputTxt.value.match(regx)){
              textField.style.color = "green";  
              span.textContent='';
          }else{
              span.textContent='';
              textField.style.color = "red";
          }  
      }else{
          span.textContent='';
          textField.style.color = "red";
      }   
  }else{
      span.textContent='';
      textField.style.color = "red";
  }
}



function lnameValidation(inputTxt){
    
  var regx = /^[a-zA-Z\s, ]+$/;
  var textField = document.getElementById("lname");
  var span = document.getElementById("ulname");
      
  if(inputTxt.value != '' ){
  
      if(inputTxt.value.length >= 0){
      
          if(inputTxt.value.match(regx)){
              textField.style.color = "green";  
              span.textContent='';
          }else{
              span.textContent='';
              textField.style.color = "red";
          }  
      }else{
          span.textContent='';
          textField.style.color = "red";
      }   
  }else{
      span.textContent='';
      textField.style.color = "red";
  }
}



function emailValidation(inputTxt){
    
  var regx = /([A-z0-9_\-\.]){1,}\@([A-z0-9_\-\.]){1,}\.([A-Za-z]){2,4}$/;
  var textField = document.getElementById("emails");
  var span = document.getElementById("emailids");
      
  if(inputTxt.value != '' ){
  
      if(inputTxt.value.length >= 0){
      
          if(inputTxt.value.match(regx)){
              textField.style.color = "green";  
              span.textContent='';
          }else{
              span.textContent='';
              textField.style.color = "red";
          }  
      }else{
          span.textContent='';
          textField.style.color = "red";
      }   
  }else{
      span.textContent='';
      textField.style.color = "red";
  }
}


function usernameValidation(inputTxt){
    
  var regx = /^[a-zA-Z\s, ]+$/;
  var textField = document.getElementById("user");
  var span = document.getElementById("username");
      
  if(inputTxt.value != '' ){
  
      if(inputTxt.value.length >= 2){
      
          if(inputTxt.value.match(regx)){
              textField.style.color = "green";  
              span.textContent='';
          }else{
              span.textContent='';
              textField.style.color = "red";
          }  
      }else{
          span.textContent='';
          textField.style.color = "red";
      }   
  }else{
      span.textContent='';
      textField.style.color = "red";
  }
}


function passwordValidation(inputTxt){
    
  var regx = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8}/;
  var textField = document.getElementById("pass");
  var span = document.getElementById("passwords");
      
  if(inputTxt.value != '' ){
  
      if(inputTxt.value.length >= 2){
      
          if(inputTxt.value.match(regx)){
              textField.style.color = "green";  
              span.textContent='';
          }else{
              span.textContent='';
              textField.style.color = "red";
          }  
      }else{
          span.textContent='';
          textField.style.color = "red";
      }   
  }else{
      span.textContent='';
      textField.style.color = "red";
  }
}


function cpasswordValidation(inputTxt){
  var textField = document.getElementById("conpass");
  var span = document.getElementById("confrmpass");
  var textField2 = document.getElementById("pass").value;
      
  if(inputTxt.value != '' ){
  
      if(inputTxt.value.length >= 2){
      
          if(inputTxt.value==textField2){
              textField.style.color = "green";  
              span.textContent='';
          }else{
              span.textContent='';
              textField.style.color = "red";
          }  
      }else{
          span.textContent='';
          // textField.style.color = "red";
      }   
  }else{
      span.textContent='';
      textField.style.color = "red";
  }
}
