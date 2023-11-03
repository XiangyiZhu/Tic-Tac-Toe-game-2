import socket
from gameboard import BoardClass


def playboard(play2, clientSocket, user_name_1):
    """
    Lets the two players play the game until the game is over.

    Args:
        play2: a variable with the type BoardClass represents the information of player2
        clientSocket: the socket object created to make a connection
        user_name_1: the user name of player 1

    """
    while play2.gameover() == False:

        print("Waiting another player's move.")
        move1 = clientSocket.recv(2014).decode("ascii") # the received move made by player 1
        play2.updateGameBoard(user_name_1, move1)

        print(f"{user_name_1}'s move:")
        play2.showboard()

        if play2.gameover():
            break
                            
        # ask and send the move to player 1
        move2 = str(input("Enter your move (eg.12 for row1column2):\n"))
        while play2.movevalid(move2) == False:
            move2 = str(input("Please enter a valid mvoe (eg.12 for row1column2):\n"))
        
        clientSocket.send(move2.encode())
        play2.updateGameBoard("player2", move2)

        play2.showboard()


def main():
    """
    The main function.
    """

    serverAddress = str(input("Enter the address\n"))
    port = int(input("Enter the port number\n"))

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverAddress, port))
    serverSocket.listen(1000)

    clientSocket, clientAddress = serverSocket.accept()

    # The received user name of player 1
    user_name_1 = clientSocket.recv(2014).decode("ascii")

    if len(user_name_1) > 0: # check whether the user name is received, and yes if True
        print(f"Receive player1's user name: {user_name_1}")
        
        clientSocket.send("player2".encode())
        play2 = BoardClass("player2", user_name_1)
                
        if_continue = "Play Again"
        while if_continue == "Play Again":

            play2.resetGameBoard()

            playboard(play2, clientSocket, user_name_1)

            print("Game Over! Wait player1 to decide play again or not")
            if_continue = clientSocket.recv(2014).decode("ascii")

    play2.printStats()
    serverSocket.close()

if __name__ == '__main__':
    main()
