#!/usr/bin/python
import sys, re, http.client, urllib.parse, urllib.parse, requests

def main():
    args = sys.argv[1:]
    if len(args) != 4:
        print ("ERROR: Invalid number of arguments")
        return 1
    
    ip = args[0]
    
    port = re.match(PORT_PATTERN, args[1], flags=0)
    if port is None:
        print ("ERROR: Invalid port")
        return 1

    coords = re.match(COORDINATE_PATTERN, args[2] + " " + args[3], flags=0)
    print (coords.group())
    if coords is None:
        print ("ERROR: Invalid Coordinates")
        return 1
    fire(ip, port.group(), coords.group())

def fire(ip, port, coords):
    parameters = {"x" : coords[0:1], "y" : coords[-1:]}

    r = requests.post("http://" + ip + ":" + port, data=parameters, timeout=30)
    r.status_code

    def update(response):
        #TODO: add the response as data to send to own server
        r = requests.post("http://localhost:5000", timeout=30)
        r.status_code
    
IP_PATTERN = "\d{3}\.\d{3}\.\d(\d{1,2})?\.\d(\d{1,2})?"
PORT_PATTERN = "^\d{1,4}"
COORDINATE_PATTERN = "\d \d"

            
if __name__ == "__main__":
    main()
