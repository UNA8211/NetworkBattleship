#!/usr/bin/python
import sys
import re

def main():
    args = sys.argv[1:]
    if len(args) != 4:
        print ("ERROR: Invalid number of arguments")
        return 1
    
    ip = re.match(IP_PATTERN, args[0], flags=0)
    if ip is None:
        print ("ERROR: Invalid IP address")
        return 1
    
    port = re.match(PORT_PATTERN, args[1], flags=0)
    if port is None:
        print ("ERROR: Invalid port")
        return 1

    coords = re.match(COORDINATE_PATTERN, args[2] + " " + args[3], flags=0)
    print (coords.group())
    if coords is None:
        print ("ERROR: Invalid Coordinates")
        return 1

IP_PATTERN = "\d{3}\.\d{3}\.\d(\d{1,2})?\.\d(\d{1,2})?"
PORT_PATTERN = "^\d{1,4}"
COORDINATE_PATTERN = "\d \d"

            
if __name__ == "__main__":
    main()
