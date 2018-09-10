# Simple Google Home Listener

Simple to use listener for IFTTT Google Assistant commands in order to control devices using Domoticz

## Setup

This is a work in progress, very crude - and my first ever git commit!

Set up IFTTT with the IF as Google Assistant and the THAT as a Web Request with a text ingredient.

Set the port that the server will listen on at the bottom of the sgh.py file.

```
app.run(host='0.0.0.0', port=<your-port-number>)
```

### IFTTT Google Assistant setup

Add the Google Assistant IF to your IFTTT Applet, and select "Say a phrase with a text ingredient".

Set the trigger text to be whatever you want - one for ON and one for OFF. Insert the $ symbol where you're going to say the name of the device.

eg: Turn off $ light
$ is the name of the device you'll say.

### IFTTT Web Request setup

The URL should be in the format:

```
http://your-remote-ip-or-dns-name:your-port/{{TextField}}/On
```

Do the same again, but with the URL as:

```
http://your-remote-ip-or-dns-name:your-port/{{TextField}}/Off
```

### Prerequisites

Tested on Ubuntu 16 and Windows 10

```
Python 2.7
Flask
ConfigParser
Requests
```

## Authors

* **Imi Votteler** - *Created through laziness*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
