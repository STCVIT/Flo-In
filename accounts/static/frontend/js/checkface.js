(function () {
    const status = (response) => {
      if (response.status >= 200 && response.status < 300) {
        return Promise.resolve(response);
      }
      return Promise.reject(new Error(response.statusText));
    };

    const json = (response) => response.json();

    // The width and height of the captured photo. We will set the
    // width to the value defined here, but the height will be
    // calculated based on the aspect ratio of the input stream.

    var width = 405; // We will scale the photo width to this
    var height = 0; // This will be computed based on the input stream

    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.

    var streaming = false;

    // The various HTML elements we need to configure or control. These
    // will be set by the startup() function.

    var video = null;
    var canvas = null;
    var startbutton = null;
    var data;

    function startup() {
      video = document.getElementById("video2");
      canvas = document.getElementById("canvas");
      startbutton = document.getElementById("startbutton");

      navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then(function (stream) {
          video.srcObject = stream;
          video.play();
        })
        .catch(function (err) {
          console.log("An error occurred: " + err);
        });

      video.addEventListener(
        "canplay",
        function (ev) {
          if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);

            // Firefox currently has a bug where the height can't be read from
            // the video, so we will make assumptions if this happens.

            if (isNaN(height)) {
              height = width / (4 / 3);
            }
            video.setAttribute("width", width);
            video.setAttribute("height", height);
            canvas.setAttribute("width", width);
            canvas.setAttribute("height", height);
            streaming = true;
          }
        },
        false
      );

      startbutton.addEventListener(
        "click",
        function (e) {
          takepicture();
          e.preventDefault();
        },
        false
      );
    }

    // Capture a photo by fetching the current contents of the video
    // and drawing it into a canvas, then converting that to a PNG
    // format data URL. By drawing it on an offscreen canvas and then
    // drawing that to the screen, we can change its size and/or apply
    // other changes before drawing it.

    function takepicture() {
      var context = canvas.getContext("2d");
      if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);
        var data = canvas.toDataURL("image/png");
      } else {
        console.log("No phot detected");
      }
      fdata = new FormData(document.getElementById("myForm"));
      var dataURI = data;
      var imageData = dataURItoBlob(dataURI);
      fdata.append("image", imageData, "{{ user.id|safe }}.png");
      fetch("/checkfacedata/", {
        method: "POST",
        body: fdata,
      })
        .then(status) // note that the `status` function is actually **called** here, and that it **returns a promise***
        .then(json) // likewise, the only difference here is that the `json` function here returns a promise that resolves with `data`
        .then((data) => {
          console.log(data);
          let save = document.getElementById("showResult");
          // ... which is why `data` shows up here as the first parameter to the anonymous function
          if (data.Success) {
            document.getElementById("showResult").innerHTML = data.Message;
            // save.style = "display:none;";
          } else {
            save.style = "display:block;";
            save.innerHTML = data.Message;
          }
        })
        .catch((error) => {
          console.log("Request failed", error);
        });
    }
    function dataURItoBlob(dataURI) {
      var byteString = atob(dataURI.split(",")[1]);
      var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
      var buffer = new ArrayBuffer(byteString.length);
      var data = new DataView(buffer);
      for (var i = 0; i < byteString.length; i++) {
        data.setUint8(i, byteString.charCodeAt(i));
      }
      return new Blob([buffer], { type: mimeString });
    }

    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener("load", startup, false);
  })();