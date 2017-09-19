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
    response = resp.text

    # sendResult takes the opponent's response to the fire POST request and
    #   creates the result POST request to the player's own server
    def sendResult():
        r = requests.post("http://localhost:5000", data=response, timeout=30)

    # if the shot was invalid, inform the client
    if resp.status_code != 200:
        print(resp.status_code, end=": ")

        if resp.status_code == 410:
            print("location (" + str(x) + "," + str(y) + ") has already recieved fire.")
        elif resp.status_code == 404:
            print("invalid coordinates entered.")
        elif resp.status_code == 400:
            print("invalid fire command attempted.")
    # if the shot was valid, ferry the result
    else:
        try:
            sendResult()
        except:
            return

IP_PATTERN = "\d{3}\.\d{3}\.\d(\d{1,2})?\.\d(\d{1,2})?"
PORT_PATTERN = "^\d{1,4}"
COORDINATE_PATTERN = "\d \d"


if __name__ == "__main__":
    main()
