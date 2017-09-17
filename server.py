from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import sys

port = None

# setup 10 x 10 matrices for player board and opponent board
ownBoard = [[""] * 10 for i in range(10)]
oppBoard = [["_"] * 10 for i in range(10)] # initialize coords with water

ownFile = ""
oppFile = "opp-board.txt" # default opposing file name

# BattleshipRequestHandler is an extension of BaseHTTPRequestHandler
class BattleshipRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

    # handles opponent fire requests and player result requests
    def do_POST(self):
        print("got POST")
        self.send_response(200)

        # determine the request's length and extract the content
        contentLen = int(self.headers.get('content-length', 0))
        content = self.rfile.read(contentLen)

        # parse the URL for the path and put the values in a map
        path = urlparse(content).path
        pathdict = parsePath(path)

        # determine what kind of request it is,
        #   fire (len = 2) or result (len > 2)
        if len(pathdict) == 2:
            resppathlist = checkFire(pathdict["x"], pathdict["y"])
            # package up and send the response
        elif len(pathdict) > 2:
            logResult(pathdict["x"], pathdict["y"], pathdict["hit"], pathdict["sink"])
        else:
            # do not raise exception,
            #   as an incorrect error path is expected behavior
            print("ERROR: Invalid URL path recieved: " + pathdict.items())


# takes in a URL path (var1=int_val&var2=int_val...)
#   and breaks up the entries into key:value pairings
def parsePath(path):
    # where the path info will be stored and returned
    pathdict = defaultdict(int)

    # find each of the fields in the URL path
    pathArr = path.split("&")
    for fvpair in pathArr:
        # separate the field and its respective value,
        #   and add the pair to the dict
        fvArr = fvpair.split("=")
        pathdict[fvArr[0]] = int(fvArr[1])

    return pathdict

# checkFire takes in a set of coordinates (target of an opponent's shot)
#   and assesses the result of the shot. This result is written to the Message.
def checkFire(x, y):
    # message process needs to be defined before this can be developed
    return "Hopefully it didn't do damage"

# logResult takes a set of coords (location of player's shot)
#   and logs the result of that shot as described by the other server
def logResult(x, y, hit, sink):

    return "must log hit, miss, sink"

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

    # TODO check if file exists. If not, error (own) or initialize file (opp)


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
    # printBoard(ownBoard)
    writeBoard("own")

    # TODO read in the opponent's board (if a game is being resumed)

    run()

if __name__ == '__main__':
    main()
