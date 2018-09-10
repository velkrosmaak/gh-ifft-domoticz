from flask import Flask
import requests
import ConfigParser

###########################################################post this to reddit

##set up the config file
conf = ConfigParser.ConfigParser()
conf.read("gh_config.ini")

#need a list of names and their associated ids

global devices
devices = {}

#read the config file
for each_section in conf.sections():
    for (each_key, each_val) in conf.items(each_section):
		#read the domoticz URL
        if each_section == "domourl":
            domourl = each_val
            print "Read Domoticz URL from config!"

        #load all the other entries in the config file
        devices.update({each_section.lower():each_val})

print devices

app = Flask(__name__)

#this function looks up the name of the device (as heard by your Google Home) and trturns the corresponding ID from the gh_config.ini file
def lookup_name2id(l_name):
    global devices
    l_name = l_name.replace("%20", " ").lower().strip()

    if l_name in devices:
        l_id = devices[l_name]
    else:
        l_id = 0
    #print "Looked up " + l_name + " and found device ID " + l_id
    return l_id

#this function changes a given Domoticz device ID to a given state (On or Off [NB: Case sensitive!])
def do_domoticz(dev_id, dev_state):
    global url
    #get the id from the name
    devid = lookup_name2id(dev_id)
    print devid
    try:
        #r = requests.get(domourl + '/json.htm?type=command&param=switchlight&idx=' + dev_id + '&switchcmd=' + dev_state)
        r = requests.get(domourl + '/json.htm?type=command&param=switchlight&idx=' + devid + '&switchcmd=' + dev_state)
        print "Sent command to Domoticz!"
        return r
    except:
        print "Error sending command to Domoticz!"

#this function changes a given Domoticz device ID to a given brightness state (On or Off [NB: Case sensitive!]). Could probably be combined with the above function.
def do_domoticz_dim(dev_id_dim, dev_state_dim):
    global url
    devid_dim = lookup_name2id(dev_id)
    try:
        r = requests.get(domourl + '/json.htm?type=command&param=switchlight&idx=' + devid_dim + '&switchcmd=Set%20Level&level=6' + dev_state_dim)
        print "Sent command to Domoticz!"
        return r
    except:
		print "Error sending command to Domoticz!"

#show an error if anyone (an attacker?) happens to hit the port you're running the flask server on
@app.route('/')
def index():
	return 'ERROR'

#the flask route for handling the call from IFTTT
@app.route('/<thing>/<state2>')
def switchhandler(thing,state2):
	#check if the state is a number for dimming
	try:
		int(state2)
		print "Setting brightness level rather than state."
		print "Dimming " + thing + " to " + state2
		do_domoticz_dim(thing, state2)
		return "OK"

	except ValueError:
		print "Turning " + thing + " " + state2
		do_domoticz(thing, state2)
		return "OK"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5055) # testing
	#app.run(host='0.0.0.0', port=5055) # "production"
