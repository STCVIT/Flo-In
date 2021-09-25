<p align="center">
    <a href="https://stcvit.in/" target="_blank"><img src="https://github.com/STCVIT/STC-README/blob/master/gitbanner.png" title="STC-VIT" alt="STC-VIT"></a>
</p>
<p align="center">
<h1><b>FLO-IN</b></h1>
<h3>FLO-IN is the smartest way to log in using facial recognition.</h3>
</p>

---

## Built With
<p float="left">
	<img src="https://github.com/STCVIT/CryptoAuction/blob/b541fecf108f1ef673d7a1f163c8eae1e2fdeffd/Build%20With/react%20png.png" alt="ReactJS" width="15%" >
	<img src="https://github.com/STCVIT/CryptoAuction/blob/b541fecf108f1ef673d7a1f163c8eae1e2fdeffd/Build%20With/trufflepng.png" alt="Truffle Blockchain" width="15%" >
	<img src="https://github.com/STCVIT/CryptoAuction/blob/b541fecf108f1ef673d7a1f163c8eae1e2fdeffd/Build%20With/node.png" alt="NodeJS" width="15%" >

</p>

---

> <Subtitle>
### FLO-IN is an extension that recognises a user whenever he/she tries to Log-In any of the accounts. The user who has registered his/her face will only be given the option to access the accounts. The face recognition will be done every time the user tries to access any of the accounts. Option to open the accounts via pattern is also provided. Hence, there is no need to Log-Out every time of the account to keep the data safe. Without any single click you can access your accounts as well as keep the account password protected.

---



## Features
* Save Password
* Auto-Fill with Facial Recognition 
* PIN Login 

<br>

## Dependencies
 - Chrome Browser
 - Python 3.8
 - Dlib

<br>

## Getting Started
- Clone the repository
```
git clone 
```
- Install the dependencies
```
pip install -r requirements.txt
```
- Start the server
```
python manage.py runserver
```

## Running this app using Docker

You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. If you're new to
Docker and want to learn it in detail check out the [additional resources
links](#learn-more-about-docker-and-django) near the bottom of this README.

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).
That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.

#### Clone this repo anywhere you want and move into the directory:

```sh
git clone link
cd FloIn

# Optionally checkout a specific tag, such as: git checkout 0.4.0
```

#### Build everything:

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python*

```sh
docker build --tag floin:latest .
```

Now that everything is built and running we can treat it like any other Django
app.

Did you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. Check out the docs
in the `.env` file for the `DOCKER_WEB_PORT_FORWARD` variable to fix this.

```sh
docker run --name floin -d -p 8000:8000 floin:latest
```

#### Setup the initial database:

```sh
./run manage migrate 
```

*We'll go over that `./run` script in a bit!*

#### Check it out in a browser:

Visit <http://localhost:8000> in your favorite browser.

Not seeing any CSS? That means Webpack is still compiling. Give it
a few more seconds and reload. It should self resolve.

<br>

## 🙌 Contributions

- Feel Free to Open a PR/Issue for any feature or bug(s).
- Make sure you follow the [community guidelines](https://docs.github.com/en/github/site-policy/github-community-guidelines)!
- Have a feature request? Open an Issue!

<br>

## ⭐ Show your support

Give a ⭐ if this tool made your life easier!

Spread the word to your geek fellows to save their time!

<br>

## ✨ Contributors
* [Vineet Raj](https://github.com/vinmik)
* [Swarup Kharul](https://github.com/SwarupKharul)
* [Vanshika Nehra](https://github.com/VanshikaNehra23)
* [Suryakant Agrawal](https://github.com/suryaa62)

## License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

## Connect with Us
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/mstcvit/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/micvitvellore/mycompany/)

[![Join Us](https://img.shields.io/badge/Join%20Us-STC-VIT)](https://stcvit.in/)

<p align="center">
	Made with :heart: by <a href="https://stcvit.in/">STC-VIT</a>
</p>
