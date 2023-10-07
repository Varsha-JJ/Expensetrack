/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function fnameValidation(inputTxt){
    
    var regx = /^[a-zA-Z\s, ]+$/;
    var textField = document.getElementById("name");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 3){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";
                    
            }else{
                textField.textContent = '**Only characters are allowed"';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = '**your firstname must include more chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = '**Please enter your firstname';
        textField.style.color = "red";
    }
}
