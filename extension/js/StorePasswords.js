console.log('hello from StorePasswords')
let token = localStorage.getItem('user')
token = JSON.parse(token)

const allURLs = [
  "https://www.facebook.com",
  "https://www.linkedin.com/login",
  "https://twitter.com/login",
  "https://www.instagram.com",
  "https://github.com/login",
  "https://vtop.vit.ac.in/vtop/initialProcess",
  "https://in.pinterest.com/",
  "https://www.reddit.com/login",
  "https://www.quora.com/",
  "https://www.netflix.com/in/login",
  "https://www.flipkart.com",
  "http://www.vpropel.in/loginn",
  "https://mail.rediff.com/cgi-bin/login.cgi",
  "https://www.irctc.co.in/nget/train-search",
  "https://www.shaadi.com",
  "https://account.similarweb.com/login",
  "https://newtrade.sharekhan.com",
  "https://moodle.org/login/index.php",
  "https://moodle.org/login/index.php",
  "https://moovit.vit.ac.in/login/index.php",
  "https://www.amazon.com/ap/signin"
]

async function sendData(url, inputUsername, encodedPassword) {
  var fdata = new FormData()

  // check if url is in the list
  allURLs.forEach(e => {
    if (url.includes(e)) {
      url = e
    }
  });
  url.charAt(url.length - 1) === '/' ? url = url.slice(0, -1) : url = url
  console.log(url)

  url = url.replace("https://", "");
  url = url.replace("http://", "");
  url = url.replace("www.", "");
  fdata.append('url', url)
  fdata.append('username', inputUsername)
  fdata.append('password', encodedPassword)
  console.log('fetching....')
  await fetch('https://flo-in2v.azurewebsites.net/api/data-create/', {
    method: 'POST',
    headers: {
      Authorization: `JWT ${token.access}`,
    },
    body: fdata,
  }).then(() => {
    console.log('data sent successfully')
    document.getElementById('msg').innerHTML = "Password Stored Successfully"
  }).catch((error) => {
    console.log(error)
    document.getElementById('msg').innerHTML = "Oops! There was some issue saving your password. Please try again!"
  })
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('contact').addEventListener('submit', function (e) {
    console.log('ubmitting...')
    e.preventDefault()
    var text = document.getElementById('passwordToStore')
    var username = document.getElementById('userName')
    try {
      chrome.tabs.query(
        { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
        function (tabs) {
          console.log('inside chrome tabs query')
          url = tabs[0].url
          sendData(url, username.value, text.value)
        },
      )
    } catch (e) {
      if (e == QUOTA_EXCEEDED_ERR) {
        alert('Quota exceeded!') //data wasn’t successfully saved due to quota exceed so throw an error
      }
    }
    // store(username.value, text.value)
  })

  function store(inputUsername, Password) {
    if (typeof localStorage == 'undefined') {
      alert('Your browser does not support HTML5 localStorage. Try upgrading.')
    } else {
      try {
        chrome.tabs.query(
          { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
          function (tabs) {
            console.log('inside chrome tabs query')
            url = tabs[0].url
            sendData(url, inputUsername, Password)
          },
        )
      } catch (e) {
        if (e == QUOTA_EXCEEDED_ERR) {
          alert('Quota exceeded!') //data wasn’t successfully saved due to quota exceed so throw an error
        }
      }
    }
  }
}
)