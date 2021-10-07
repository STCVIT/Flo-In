// make the request to the login endpoint
const userElement = document.getElementById('email');
const passwordElement = document.getElementById('password');
const trigger = document.getElementById('trigger');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

trigger.addEventListener('click', (e) => {
    e.preventDefault();
    var loginUrl = 'https://flo-in2v.azurewebsites.net/api/authenticate/jwt/create/'
    var email = userElement.value;
    var password = passwordElement.value;
    console.log("hi")
    fetch(loginUrl, {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": email,
            "password": password,
        })
    }).then(res => res.json()).then(res => {
        let inMemoryToken = res.token;
        localStorage.setItem('user', JSON.stringify(res));
        if ('access' in res) {
            window.location.href = "popup.html";
        }
        return inMemoryToken;
    })
})