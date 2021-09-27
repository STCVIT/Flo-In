const FULL_DASH_ARRAY = 283;
  const WARNING_THRESHOLD = 4;
  const ALERT_THRESHOLD = 2;
  let stopRec;

  const record = document.getElementById("record");
  const stop = document.getElementById("stop");
  const form = document.getElementById("myForm");

  if (!navigator.mediaDevices) {
    alert("getUserMedia support required to use this page");
  }

  const chunks = [];
  let onDataAvailable = (e) => {
    chunks.push(e.data);
  };

  // Not showing vendor prefixes.
  navigator.mediaDevices
    .getUserMedia({
      audio: false,
      video: true,
    })
    .then((mediaStream) => {
      const recorder = new MediaRecorder(mediaStream);
      recorder.ondataavailable = onDataAvailable;
      const video = document.querySelector("video");
      video.srcObject = mediaStream;
      record.onclick = () => {
        recorder.start();
        console.log(recorder.state);
        startTimer();
        console.log("recorder started");
      };

      stopRec = () => {
        recorder.stop();
        console.log(recorder.state);
        console.log("recorder stopped");
      };

      video.onloadedmetadata = (e) => {
        console.log("onloadedmetadata", e);
      };

      recorder.onstop = (e) => {
        console.log("e", e);
        console.log("chunks", chunks);
        const bigVideoBlob = new Blob(chunks, {
          type: "video/mp4",
          codecs: "avc1.42001E, mp4a.40.2",
        });
        var file = new File([bigVideoBlob], "{{ user.id|safe }}.mp4", {
          type: "video/mp4",
          codecs: "avc1.42001E, mp4a.40.2",
          lastModified: Date.now(),
        });

        let fd = new FormData(form);
        fd.append("data", file);
        fetch("/facedata/", {
          method: "POST",
          body: fd,
        })
          .then((res) => res.json())
          .then((res) => {
            console.log(res);
            let save = document.getElementById("alert_save_face");
            let not_save = document.getElementById("alert_save_face_not");
            if (res.Success == true) {
              save.style = "display:block;";
              save.innerHTML = res.Message;
              not_save.style = "display:none;";
            } else {
              not_save.style = "display:block;";
              not_save.innerHTML = res.Message;
              save.style = "display:none;";
            }
            console.log("fetching done");
            // window.location.reload();
          });
      };
    })
    .catch(function (err) {
      console.log("error", err);
    });

  const COLOR_CODES = {
    info: {
      color: "green",
    },
    warning: {
      color: "orange",
      threshold: WARNING_THRESHOLD,
    },
    alert: {
      color: "red",
      threshold: ALERT_THRESHOLD,
    },
  };

  let TIME_LIMIT = 3;
  let timePassed = 0;
  let timeLeft = TIME_LIMIT;
  let timerInterval = null;
  let remainingPathColor = COLOR_CODES.info.color;

  document.getElementById("app").innerHTML = `
  <div class="base-timer">
    <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g class="base-timer__circle">
        <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
        <path
          id="base-timer-path-remaining"
          stroke-dasharray="283"
          class="base-timer__path-remaining ${remainingPathColor}"
          d="
            M 50, 50
            m -45, 0
            a 45,45 0 1,0 90,0
            a 45,45 0 1,0 -90,0
          "
        ></path>
      </g>
    </svg>
    <span id="base-timer-label" class="base-timer__label">${formatTime(
      timeLeft
    )}</span>
  </div>
  `;

  function onTimesUp() {
    stopRec();
    clearInterval(timerInterval);
    TIME_LIMIT = 3;
    timePassed = 0;
    timeLeft = TIME_LIMIT;
    timerInterval = null;
    remainingPathColor = COLOR_CODES.info.color;
    document.getElementById("app").innerHTML = `
  <div class="base-timer">
    <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g class="base-timer__circle">
        <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
        <path
          id="base-timer-path-remaining"
          stroke-dasharray="283"
          class="base-timer__path-remaining ${remainingPathColor}"
          d="
            M 50, 50
            m -45, 0
            a 45,45 0 1,0 90,0
            a 45,45 0 1,0 -90,0
          "
        ></path>
      </g>
    </svg>
    <span id="base-timer-label" class="base-timer__label">${formatTime(
      timeLeft
    )}</span>
  </div>
  `;
  }

  function startTimer() {
    timerInterval = setInterval(() => {
      timePassed = timePassed += 1;
      timeLeft = TIME_LIMIT - timePassed;
      document.getElementById("base-timer-label").innerHTML =
        formatTime(timeLeft);
      setCircleDasharray();
      setRemainingPathColor(timeLeft);

      if (timeLeft === 0) {
        onTimesUp();
      }
    }, 1000);
  }

  function formatTime(time) {
    const minutes = Math.floor(time / 60);
    let seconds = time % 60;

    if (seconds < 10) {
      seconds = `0${seconds}`;
    }

    return `${minutes}:${seconds}`;
  }

  function setRemainingPathColor(timeLeft) {
    const { alert, warning, info } = COLOR_CODES;
    if (timeLeft <= alert.threshold) {
      document
        .getElementById("base-timer-path-remaining")
        .classList.remove(warning.color);
      document
        .getElementById("base-timer-path-remaining")
        .classList.add(alert.color);
    } else if (timeLeft <= warning.threshold) {
      document
        .getElementById("base-timer-path-remaining")
        .classList.remove(info.color);
      document
        .getElementById("base-timer-path-remaining")
        .classList.add(warning.color);
    }
  }

  function calculateTimeFraction() {
    const rawTimeFraction = timeLeft / TIME_LIMIT;
    return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
  }

  function setCircleDasharray() {
    const circleDasharray = `${(
      calculateTimeFraction() * FULL_DASH_ARRAY
    ).toFixed(0)} 283`;
    document
      .getElementById("base-timer-path-remaining")
      .setAttribute("stroke-dasharray", circleDasharray);
  }