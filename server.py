from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from re import sub
from urllib.parse import urlencode, urlparse
import sys

port = None

# setup 10 x 10 matrices for player board and opponent board
ownBoard = [[""] * 10 for i in range(10)]
oppBoard = [["_"] * 10 for i in range(10)] # initialize coords with water

# tracking remaining hits on each ship
shipStatus = defaultdict(int)

ownFile = ""
oppFile = "opp-board.txt" # default opposing file name

# BattleshipRequestHandler is an extension of BaseHTTPRequestHandler
class BattleshipRequestHandler(BaseHTTPRequestHandler):
    # handles opponent fire requests and player result requests
    def do_POST(self):
        # determine the request's length and extract the content
        contentLen = int(self.headers.get('content-length', 0))
        content = self.rfile.read(contentLen)

        # parse the URL for the path.
        # sanitize it
        # put the values in a map
        pathdict = parsePath(sub("b","",sub("'","",str(urlparse(content).path))))

        # determine what kind of request it is,
        #   fire (len = 2) or result (len > 2)
        if len(pathdict) == 2:
            respdict = handleFire(int(pathdict["x"]), int(pathdict["y"]))

            # package up and send the response
            sendResponse(self, respdict)
        elif len(pathdict) > 2:
            self.send_response(200)
            handleResult(int(pathdict["x"]), int(pathdict["y"]), int(pathdict["hit"]), pathdict["sink"])
        else:
            # do not raise exception,
            #   as an invalid fire command is expected behavior
            print("ERROR: Invalid URL path recieved: " + pathdict.items())
            self.send_response(400)

# sendResponse forms and sends an HTTP response
def sendResponse(self, respdict):
    self.send_response(int(respdict["status_code"]))
    self.send_header("Content-type", "text/plain")
    self.end_headers()

    del respdict["status_code"]
    self.wfile.write(urlencode(respdict).encode("utf-8"))
    #self.wfile.close()

# takes in a URL path (var1=int_val&var2=int_val...)
#   and breaks up the entries into key:value pairings
def parsePath(path):
    # where the path info will be stored and returned
    pathdict = defaultdict(str)

    # find each of the fields in the URL path
    pathArr = path.split("&")
    for fvpair in pathArr:
        # separate the field and its respective value,
        #   and add the pair to the dict
        fvArr = fvpair.split("=")
        pathdict[fvArr[0]] = fvArr[1]

    return pathdict

# checkFire takes in a set of coordinates (target of an opponent's shot)
#   and assesses the result of the shot. This result is written to the Message.
def handleFire(x, y):
    # keep track of the response information to return
    respdict = defaultdict(str)
    respdict["x"] = x
    respdict["y"] = y
    respdict["hit"] = 0

    global ownBoard
    global shipStatus

    # 404 if the coordinates cannot be found
    if x < 0 or x >= len(ownBoard) or y < 0 or y >= len(ownBoard[x]):
        respdict["status_code"] = 404 # Not Found
        return respdict

    respdict["status_code"] = 200 # Ok

    # check if the square has been fired at already
    if ownBoard[x][y] == "X":
        respdict["status_code"] = 410 # Gone
    # if a ship has been hit
    elif ownBoard[x][y] != "_":
        # log a hit on whatever ship was hit
        respdict["hit"] = 1
        shipStatus[ownBoard[x][y]] -= 1

        # check if the ship has been sunk
        if shipStatus[ownBoard[x][y]] == 0:
            respdict["sink"] = ownBoard[x][y]

    # mark the position as having been fired at
    ownBoard[x][y] = "X"
    # writeBoard("own") # comment this out to disable persisting

    # return what will be the contents of the response message
    return respdict

# logResult takes a set of coords (location of player's shot)
#   and logs the result of that shot as described by the other server
def handleResult(x, y, hit, sink):
    global oppBoard

    # determine what mark should be placed on the board
    mark = "M"
    if sink > 0:
        mark = "S"
    elif hit > 0:
        mark = "H"

    oppBoard[x][y] = mark
    # writeBoard("opp") # comment this out to disable persisting

# readBoard takes a file representing a board
#   and reads it into the given 10 x 10 matrix
def readBoard(boardName):
    # check arguments & assign proper file/matrix to use
    f = ""
    b = None
    if boardName == "own":
        f = ownFile
        b = ownBoard
    elif boardName == "opp":
        f = oppFile
        b = oppBoard
    else:
        raise Exception("Expected \"own\" or \"opp\" as arg. Got " + board)

    # open the file and populate the board
    with open(f, 'r') as boardFile:
        x = 0
        for line in boardFile:
            # go through each character in the line and populate the board
            for y in range(10):
                b[x][y] = line[y]
            x += 1

# readBoard takes a 10 x 10 matrix representing a board
#   and writes it to the given file
def writeBoard(boardName):
    # check arguments & assign proper file/matrix to use
    f = ""
    b = None
    if boardName == "own":
        f = ownFile
        b = ownBoard
    elif boardName == "opp":
        f = oppFile
        b = oppBoard
    else:
        raise ValueError("Expected \"own\" or \"opp\" as arg. Got " + board)

    # open the file and populate the board
    with open(f, 'w') as boardFile:
        for x in range(len(b)):
            # go through each character in the line and populate the board
            for y in range(len(b[x])):
                # i is the ROW number, j is the COLUMN number
                boardFile.write(str(b[x][y]))
            boardFile.write("\n")

    # additionally, write the board to the HTML file
    #writeBoardToHTML(b, f)

# writeBoardToHTML writes the given board
def writeBoardToHTML(board, txtfilename):
    raise Exception("Don't use me. I don't do anything yet.")

# printBoard takes in the board to print and prints it
def printBoard(board):
    for x in range(len(board)):
        for y in range(len(board[x])):
            print(board[x][y], end="")
        print()
    print()

# run sets up the desired server and runs it
def run(server_class=HTTPServer, handler_class=BattleshipRequestHandler):
    server_address = ('', port)
    server = server_class(server_address, handler_class)
    print("Standing up Battleship server...")

    try:
    	server.serve_forever()
    except KeyboardInterrupt:
    	pass

    server.server_close()
    print("Shutting down Battleship server...")

def main():
    global port
    global ownFile
    if len(sys.argv) != 3:
        print("ERROR: You must provide the port and the board file to stand up a server.")
        return 1

    # read in the args from the command line
    port = int(sys.argv[1])
    ownFile = sys.argv[2]

    # read in the player's board
    readBoard("own")
    shipStatus["C"] = 5
    shipStatus["B"] = 4
    shipStatus["R"] = 3
    shipStatus["S"] = 3
    shipStatus["D"] = 2

    # TODO read in the opponent's board (if a game is being resumed)

    run()

if __name__ == '__main__':
    main()
