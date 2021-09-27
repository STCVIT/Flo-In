function pincode() {
    var input = document.getElementById("userInput").value;
    console.log(document.getElementById("userInput").type)
    fdata = new FormData(document.getElementById("PINform"));
    console.log(fdata)
    fetch("setpattern/", {
        method: "POST",
        body: fdata,
    })
        .then((res) => res.json()) // note that the `status` function is actually **called** here, and that it **returns a promise***
        .then((res) => {
            console.log(res.Success);
            let save = document.getElementById("showPINSuccessResult");
            let fail = document.getElementById("showPINFailResult");
            // ... which is why `res` shows up here as the first parameter to the anonymous function
            if (res.Success) {
                save.style.display = "block";
                save.innerHTML += res.Message;
                fail.style.display = "none";
            } else {
                fail.style.display = "block";
                fail.innerHTML += res.Message;
                save.style.display = "none";
            }
        })
        .catch((error) => {
            console.log("Request failed", error);
        });
}
function showPassword() {
    // document.getElementById("userInput").type = "text";
    var eye = document.getElementById("eyeb");
    if (document.getElementById("userInput").type === "password") {
        //     // eye.innerHTML=="&#xf070;" eye.innerHTML="&#xf06e;";
        //     alert("hi");
        document.getElementById("userInput").type = "text";


    }
    else {
        document.getElementById("eyeb").innerText = "&#xf06e;"
        document.getElementById("userInput").type = "password";

    }


}

// jQuery.noConflict();
// $(document).ready(function (e) {
//     $(function () {
//         $("input[name='password']").on('input', function (e) {
//             $(this).val($(this).val().replace(/[^0-9]/g, ''));
//         });
//     });




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
    // $('#userInput, #userInput2').on('keyup', function () {
    //     if ($('#userInput').val() == $('#userInput2').val()) {
    //         $('#message').html('').css('color', '#eee');
    //     } else
    //         $('#message').html('pins do not match! ').css('color', '#eee');
    // });
    // $(".showpass").click(function () {
    //     $(this).toggleClass("fa-eye fa-eye-slash");
    //     input = $("#userInput");
    //     if (input.attr("type") == "password") {
    //         input.attr("type", "text");
    //     } else {
    //         input.attr("type", "password");
    //     }
    // });
// }
// )