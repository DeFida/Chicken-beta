// function make_sidebar_button_selected(selected_sidebar_button_name, selected_sidebar_button_id) {
//   document.getElementById(selected_sidebar_button_id).classList.remove("back-question-box_selected");
//   document.getElementsByName(selected_sidebar_button_name).classList.add("back-question-box_selected");
// }

function show_navbar__user_options() {
  document.getElementById("navbar__user-options").classList.toggle("show");
}


function side_bar_button_click(id) {
  var buttons = document.getElementsByName("side_bar_button");
  var i;
  for (i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove("back-question-box_clicked");
  }
  console.log("button is clicked");
  document.getElementById(id).classList.toggle("back-question-box_clicked");
}

window.onclick = function(event) {
  if (!event.target.matches('.navbar__user-block__img')) {
    var dropdowns = document.getElementsByClassName("navbar__user-options");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        
        openDropdown.classList.remove('show');
      };
    };
  };
};

function submit_sign_up(){
  var username = document.getElementById("username");
  var email = document.getElementById("email");
  var password = document.getElementById("password");

  

  var sign_up = {
      username: username.value,
      email: email.value, 
      password: password.value
  };

  fetch('/sign_up/', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(sign_up), 
      cache: "no-cache", 
      headers: new Headers({
          "content-type": "application/json"
      })
  });
  

  fetch('/sign_up/')
    .then(function (response) {
      return response.json(); // But parse it as JSON this time
  })
  .then(function (json) {
      console.log(json); // Here’s our JSON object
  })
      // response.json().then(function(data){
      //     var err;
      //     err = data[0]["error"];
      //     console.log(err);
      //     if (err == "username_err"){
              
      //         document.getElementById("username_err").style = "display: block; color: red;";
      //         document.getElementById("email_err").style = "display: none;";
      // }
      //     else if (err == "email_err"){
      //         document.getElementById("username_err").style = "display: none;";

      //         document.getElementById("email_err").style = "display: block; color: red;";
      // }
      //     else if (err == "none"){
      //         document.getElementById("email_err").style = "display: none;";
      //         document.getElementById("username_err").style = "display: none;";
      // }
      // });
      
      
};
