function pincode() {

    var input = document.getElementById("userInput").value;
    var input2 = document.getElementById("userInput2").value;
    fdata = new FormData(document.getElementById("PINform"));
    console.log(fdata)
    if (input === input2) {
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
                    save.getElementById("tick2").innerHTML = res.Message;
                    fail.style.display = "none";
                } else {
                    fail.style.display = "block";
                    fail.getElementById("cross2").innerHTML = res.Message;
                    save.style.display = "none";
                }
            })
            .catch((error) => {
                console.log("Request failed", error);
            });
    }
    else {
        alert("PINs do not match")
    }

}
function showPassword() {

    var eye = document.getElementById("eyeb");
    var span = document.getElementById("eyespan")
    if (document.getElementById("userInput").type === "password") {
        //span.innerHTML=='<i style="color: #eee" id="eyeb" class="fa">&#xf070;</i></span>';

        document.getElementById("userInput").type = "text";


    }
    else {
        //span.innerHTML = '<i style="color: #eee" id="eyeb" class="fa">&#xf06e;</i></span>';
        document.getElementById("userInput").type = "password";

    }


}

