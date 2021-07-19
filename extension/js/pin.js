let trigger = document.getElementById('submitpin');
let token = localStorage.getItem('user')
token = JSON.parse(token)

function autofill() {
    chrome.tabs.query({ 'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT },
        function (tabs) {
            console.log(tabs[0]);
            url = tabs[0].url;
            fetch(`http://127.0.0.1:8000/api/data-detail/${url}/`, {
                method: 'get',
                headers: {
                    Authorization: `JWT ${token.access}`,
                }
            }).then(res => res.json()).then(res => {
                var userdata = JSON.parse(JSON.stringify(res))
                username = userdata.username
                password = userdata.password
                let someJSON = { "userName": username, "password": password };
                console.log(userdata)
                console.log(someJSON)
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
                        console.log("hello")
                        document.getElementsByTagName("button")[0].click();
                        return { success: true, html: document.body.innerHTML };
                    } + ')(' + JSON.stringify(someJSON) + ');'
                });
            })
        });
};


trigger.addEventListener('click', async (e) => {
    e.preventDefault();
    let PIN = document.getElementById("userInput").value;
    var fdata = new FormData()
    fdata.append('pin', PIN)
    await fetch('http://127.0.0.1:8000/api/checkpattern/', {
        method: 'POST',
        headers: {
            Authorization: `JWT ${token.access}`,
        },
        body: fdata,
    }).then(res => { console.log(res); res.json() }).then(res => {
        var auth = JSON.parse(JSON.stringify(res))
        console.log(res);
        if (auth.match == "Matched") {
            autofill()
        }
        else {
            document.getElementById("err").innerHTML = "PIN Not Matched";
        }
    }).catch((error) => {
        console.log(error)
    })
}
)