// The width and height of the captured photo. We will set the
// width to the value defined here, but the height will be
// calculated based on the aspect ratio of the input stream.
console.log('hi from popup js')
var width = 320 // We will scale the photo width to this
var height = 0 // This will be computed based on the input stream

// |streaming| indicates whether or not we're currently streaming
// video from the camera. Obviously, we start at false.

var streaming = false

// The various HTML elements we need to configure or control. These
// will be set by the startup() function.

var video = null
var canvas = null
var startbutton = null
let data
let logout = document.getElementById('logout')
let token

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


window.onload = () => {
  if (localStorage.getItem('user')) {
    try {
      token = localStorage.getItem('user')
      token = JSON.parse(token)
      if ('access' in token) {
        fd = new FormData()
        fd.append('token', token.access)
        fetch('http://127.0.0.1:8000/api/authenticate/jwt/verify/', {
          method: 'POST',
          body: fd
        }).then(res => {
          if (res.status == 401) {
            window.location.href = 'login.html'
          }
        })
      }
      else {
        console.log("access")
        window.location.href = 'login.html'
      }
    } catch (error) {

    }
  }
  else {
    console.log("login")
    window.location.href = 'login.html'
  }
}


function startup() {
  video = document.getElementById('webcamVideo')
  canvas = document.getElementById('canvas')
  photo = document.getElementById('photo')
  startbutton = document.getElementById('startbutton')

  navigator.mediaDevices
    .getUserMedia({ video: true, audio: false })
    .then(function (stream) {
      video.srcObject = stream
      video.play()
    })
    .catch(function (err) {
      console.log('An error occurred: ' + err)
    })

  video.addEventListener(
    'canplay',
    function (ev) {
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width)

        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.

        if (isNaN(height)) {
          height = width / (4 / 3)
        }
        video.setAttribute('width', width)
        video.setAttribute('height', height)
        canvas.setAttribute('width', width)
        canvas.setAttribute('height', height)
        streaming = true
      }
    },
    false,
  )

  startbutton.addEventListener(
    'click',
    function (ev) {
      takepicture()
      ev.preventDefault()
    },
    false,
  )
}

// Capture a photo by fetching the current contents of the video
// and drawing it into a canvas, then converting that to a PNG
// format data URL. By drawing it on an offscreen canvas and then
// drawing that to the screen, we can change its size and/or apply
// other changes before drawing it.

function takepicture() {
  var context = canvas.getContext('2d')
  if (width && height) {
    canvas.width = width
    canvas.height = height
    context.drawImage(video, 0, 0, width, height)
    console.log(canvas)
    console.log(context)
    data = canvas.toDataURL('image/png')
  } else {
    console.log('No photo detected')
  }
  var fdata = new FormData()
  var dataURI = data
  var imageData = dataURItoBlob(dataURI)
  // data.append( 'csrfmiddlewaretoken', getCookie('CSRF-TOKEN') );
  fdata.append('image', imageData, '123.png')
  fetch('http://127.0.0.1:8000/api/upload/', {
    method: 'POST',
    headers: {
      Authorization: `JWT ${token.access}`,
    },
    body: fdata,
  }).then(res => res.json()).then(res => {
    var auth = JSON.parse(JSON.stringify(res))
    console.log(auth.match)
    if (auth.match == "Authorised") {
      autofill()

    }
  }).catch((error) => {
    console.log(error)
  })
}
function dataURItoBlob(dataURI) {
  var byteString = atob(dataURI.split(',')[1])
  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
  var buffer = new ArrayBuffer(byteString.length)
  var data = new DataView(buffer)
  for (var i = 0; i < byteString.length; i++) {
    data.setUint8(i, byteString.charCodeAt(i))
  }
  return new Blob([buffer], { type: mimeString })
}
// Set up our event listener to run the startup process
// once loading is complete.
window.addEventListener('load', startup, false)

logout.onclick = async function () {
  var fdata = new FormData()
  fdata.append('refresh', token.refresh)
  console.log(token.refresh)
  await fetch('http://127.0.0.1:8000/api/logout/', {
    method: 'POST',
    headers: {
      Authorization: `JWT ${token.access}`,
    },
    body: fdata,
  }).then(() => {
    console.log('Logout successfull')
  })
  localStorage.removeItem('user')
  window.location.href = 'login.html'
}

function patterncheck() {
  var fdata = new FormData()
  fdata.append('image', imageData, '123.png')
  fetch('http://127.0.0.1:8000/api/upload/', {
    method: 'POST',
    headers: {
      Authorization: `JWT ${token.access}`,
    },
    body: fdata,
  }).then(res => res.json()).then(res => {
    var auth = JSON.parse(JSON.stringify(res))
    console.log(auth.match)
    if (auth.match == "Authorised") {
      autofill()
    }
  }).catch((error) => {
    console.log(error)
  })
}

