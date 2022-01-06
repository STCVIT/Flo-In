
function pincode() {

    var input = document.getElementById("userInput").value;
    var input2 = document.getElementById("userInput2").value;

    fdata = new FormData(document.getElementById("PINform"));
    if (input === input2) {
        fetch("setpattern/", {
            method: "POST",
            body: fdata,
        })
            .then((res) => res.json())
            .then((res) => {
                console.log(res);
                let save = document.getElementById("showPINSuccessResult");
                let fail = document.getElementById("showPINFailResult");
                if (res.Success) {
                    save.style.display = "block";
                    document.getElementById("tick3").innerHTML = res.Message;
                    setTimeout(function () { save.style.display = "none"; }, 3000);
                    fail.style.display = "none";
                } else {
                    fail.style.display = "block";
                    document.getElementById("cross3").innerHTML = res.Message;
                    console.log(res.Message)
                    setTimeout(function () { fail.style.display = "none"; }, 3000);
                    save.style.display = "none";
                }
            })
            .catch((error) => {
                console.log("Request failed", error);
            });
    }
    else {
        let save = document.getElementById("showPINSuccessResult");
        let fail = document.getElementById("showPINFailResult");
        fail.style.display = "block";
        document.getElementById("cross3").innerHTML = "PIN's don't match, Please try again!";
        save.style.display = "none";
    }
}

function showPassword() {

    var eye = document.getElementById("eyeb");
    var span = document.getElementById("eyespan")
    if (document.getElementById("userInput").type === "password") {
        span.innerHTML = '<i style="color: #eee" id="eyeb" class="fa">&#xf070;</i></span>';
        document.getElementById("userInput").type = "text";


    }
    else {
        span.innerHTML = '<i style="color: #eee" id="eyeb" class="fa"> &#xf06e; </i></span>';
        document.getElementById("userInput").type = "password";

    };


}

