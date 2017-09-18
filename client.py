#!/usr/bin/python
import sys, re, http.client, requests

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

    fire(ip, port.group(), args[2], args[3])

def fire(ip, port, x, y):
    parameters = {"x" : x, "y" : y}

    resp = requests.post("http://" + ip + ":" + port, data=parameters, timeout=30)
    print(resp.status_code)

    def sendResult():
        #TODO: add the response as data to send to own server
        r = requests.post("http://localhost:5000", data=resp.text, timeout=30)
        print(r.status_code)
        if r.status_code != 200:
            print("ERROR: your server could not be updated with the results of the shot.")

    if resp.status_code == 200:
        sendResult()

IP_PATTERN = "\d{3}\.\d{3}\.\d(\d{1,2})?\.\d(\d{1,2})?"
PORT_PATTERN = "^\d{1,4}"
COORDINATE_PATTERN = "\d \d"


if __name__ == "__main__":
    main()
