jQuery.noConflict();
$(document).ready(function(e){
$(function () {
    $("input[name='password']").on('input', function (e) {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
});

function pincode() {
    var input = document.getElementById("userInput").value;
    alert(input);
}

 function showpass() {
    document.getElementById("userInput").type="text";
    // var eye=document.getElementById("eyeb");
    // if (document.getElementById("userInput").type="password"){
    //     // eye.innerHTML=="&#xf070;" eye.innerHTML="&#xf06e;";
    //     alert("hi");
    //      document.getElementById("userInput").type="text";
    //      return true; }
    // else{
    //         document.getElementById("userInput").type="password";
    //     }
    
     
  }

// function match(){
//     var og= document.getElementById("userInput").value;
//     var conf= document.getElementById("userInput2").value;
//     if (og===conf){
//         console.log(true);
//     }
//     else{
//         console.log("not working");
//     }
// }
$('#userInput, #userInput2').on('keyup', function () {
    if ($('#userInput').val() == $('#userInput2').val()) {
        $('#message').html('').css('color', '#eee');
    } else
        $('#message').html('pins do not match! ').css('color', '#eee');
});
$(".showpass").click(function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    input = $("#userInput");
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
});
}
)