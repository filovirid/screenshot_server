# SCREENSHOT_SERVER
Ready-to-use server to capture screenshots, HTML source code, HAR logs, page title and destination URL using chromedriver and python selenium library.

It uses:
1. Google Chrome browser and driver.
3. Python 3 CherryPy framework as web server.
4. Python 3 Selenium library.

## Installation

1. First clone the repository
```bash 
git clone https://github.com/filovirid/screenshot_server.git
cd screenshot_server
```
2. Then use docker command (takes a few minutes to install libraries).
```bash
docker build -t myimage .
```
3. After successful installation, run the container.
```bash
docker container run --rm -it -d --user screenshot -p 8000:8086 --name scrshot_container myimage
```
4. Now you can visit http://localhost:8000 to see the API page and documentation.
5. If you are installing it on a server (e.g., VPS), use server IP address instead of 'localhost'.

#### Example
1. Enter the following URL in the browser.
(Capturing screenshot and HTML and HAR log of Google.com)
```bash
http://localhost:8000/api?url=http://google.com&token=5d6b091416885eaa91283321b69dc526fc42c97783e4cdfdff7a945e3be1f9ef
```

#### Configuration (read it before using this project!!!).
1. If you do not need to collect HAR logs, it is **recommended** to disable it by changing the configuration in src/sc_config.py file. 
2. After cloning the repo, it's possible to add/remove/edit the default tokens in src/tokens.py
3. Note that the token length **must** be exactly **64** characters.


