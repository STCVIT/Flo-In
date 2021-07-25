console.log('hello from StorePasswords')
let token = localStorage.getItem('user')
token = JSON.parse(token)

async function sendData(url, inputUsername, encodedPassword) {
  var fdata = new FormData()
  fdata.append('url', url)
  fdata.append('username', inputUsername)
  fdata.append('password', encodedPassword)
  console.log('fetching....')
  await fetch('http://localhost:8000/api/data-create/', {
    method: 'POST',
    headers: {
      Authorization: `JWT ${token.access}`,
    },
    body: fdata,
  }).then(() => {
    console.log('data sent successfully')
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