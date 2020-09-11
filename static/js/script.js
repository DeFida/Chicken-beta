var username = document.getElementById("username");
var username_len = document.getElementById("username_len");

username.addEventListener("keyup", function() {
    var characters = username.value.split('');
    username_len = characters.length;
})