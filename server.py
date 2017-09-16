# setup 10 x 10 matrices for player board and opponent board (Python is stupid)
ownBoard = [[""] * 10 for i in range(10)]
oppBoard = [[""] * 10 for i in range(10)]

ownFile = "board.txt"
oppFile = "opp-board.txt"

# checkFire takes in a set of coordinates (target of an opponent's shot)
#   and assesses the result of the shot. This result is written to the Message.
def checkFire(x, y):
    # message process needs to be defined before this can be developed
    return "Hopefully it didn't do damage"

# readBoard takes a file representing a board
#   and reads it into the given 10 x 10 matrix
def readBoard(board):
    # check arguments & assign proper file/matrix to use
    f = ""
    b = None
    if board == "own":
        f = ownFile
        b = ownBoard
    elif board == "opp":
        f = oppFile
        b = oppBoard
    else:
        raise ValueError("Expected \"own\" or \"opp\" as arg. Got " + board)

    # open the file and populate the board
    with open(f, 'r') as boardFile:
        x = 0
        for line in boardFile:
            # go through each character in the line and populate the board
            for y in range(10):
                # i is the ROW number, j is the COLUMN number
                b[x][y] = line[y]


# readBoard takes a 10 x 10 matrix representing a board
#   and writes it to the given file
def writeBoard(board, file):
    return "show bob and vagene"

def main():
    print("Server functionality not supported")

if __name__ == '__main__':
    main()
