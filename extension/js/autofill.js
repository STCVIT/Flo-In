var userName = "aekjf";
var decrypted = ":AKufh";

// fdata	= new FormData();
//     var dataURI	= data;
//     var imageData   = dataURItoBlob( dataURI );
//     fdata.append( "image", imageData, "{{ user.id|safe }}.png" );
//     fetch('/checkfacedata/', {
//     method: 'POST',
//     body: fdata
//     }).then(status)    // note that the `status` function is actually **called** here, and that it **returns a promise***
//   .then(json)      // likewise, the only difference here is that the `json` function here returns a promise that resolves with `data`
//   .then(data => {  // ... which is why `data` shows up here as the first parameter to the anonymous function
//     console.log(data.match)
//     document.getElementById("showResult").innerHTML = data.match;
//   })
//   .catch(error => {
//     console.log('Request failed', error)
//   })

window.onload = function () {
    document.getElementById("Fill").onclick = function autofill() {
        chrome.tabs.query({ 'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT },
            function (tabs) {
                console.log(tabs[0]);
                url = tabs[0].url;
                var value = localStorage.getItem(url);
                console.log(value);
                var TempValue = value.split("0+/");
                userName = TempValue[0];
                var passwordValue = TempValue[1];
                decrypted = CryptoJS.AES.decrypt(passwordValue, "Secret Passphrase").toString(CryptoJS.enc.Utf8);
                var someJSON = { "userName": userName, "password": decrypted };

                chrome.tabs.executeScript({
                    code: '(' + function (params) {
                        var inputs = document.getElementsByTagName("input");
                        for (var i = 1; i < inputs.length; i++) {
                            if (inputs[i].type == "password") {
                                inputs[i - 1].value = params.userName;
                                inputs[i].value = params.password;
                                break;
                            }
                        }
                        return { success: true, html: document.body.innerHTML };
                    } + ')(' + JSON.stringify(someJSON) + ');'
                }, function (results) {
                });
            });
    };
};
