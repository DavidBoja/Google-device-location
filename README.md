# Google device location

Python 3 script that uses Selenium to query Google's "Find my phone" website to obtain your device's (device with a google account assigned to it) location (latitude and longitude).

### Usage
```
python3 get_mobile_location.py GMAIL GMAIL_PASSWORD DEVICE_NAME --LOCALLY
```
where:
1. GMAIL = your gmail address
2. GMAIL_PASSWORD = your gmail address password
3. DEVICE_NAME = the device that has the google account assigned to it. The name must be precise as on the Google's "Find my phone" site
4. --LOCALLY = Optional flag. If True, the script opens the google 

or rather:
```
latitude, longitude = get_location(GMAIL, GMAIL_PASSWORD, DEVICE_NAME, LOCALLY)
```
within python.

### Dependencies
You can use
```
pip install selenium
```
to install Selenium package into the appropriate env.

### HEROKU
If the flag --HEROKU is added, the script can be run in gui-less environment like Heroku. This flag only changes the way chrome is run, that is now windowless.
There are additional settings to be set. You need to setup an environmental variable GOOGLE_CHROME_BIN for the chromedriver parameters which adds shims after installing the following Buildpacks on Heroku:
1. https://github.com/heroku/heroku-buildpack-chromedriver.git
2. https://github.com/heroku/heroku-buildpack-google-chrome.git

which allows the line:
```
opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
```
to function. (Usually it's '/app/.apt/usr/bin/google-chrome').

The setup for other gui-less env's is probably similar.
