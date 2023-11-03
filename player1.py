import socket
from gameboard import BoardClass


def playboard(play1, connectionSocket, user_name_1):
    """
    Lets the two players play the game until the game is over.

    Args:
        play1: a variable with the type BoardClass represents the information of player1
        clientSocket: the socket object created to make a connection
        user_name_1: the user name of player 1

    """
    while play1.gameover() == False:
        # move made by player 1
        move = str(input("Enter your move (eg.12 for row1column2):\n"))

        while play1.movevalid(move) == False:
            move = str(input("Please enter a valid move (eg.12 for row1column2):\n"))

        play1.updateGameBoard(user_name_1, move)
        connectionSocket.send(move.encode())

        play1.showboard()

        if play1.gameover():
            break

        print("Waiting another player's move.")
        move2 = connectionSocket.recv(1024).decode("ascii") # the received move made by player 2
        play1.updateGameBoard("player2", move2)

        print("player2's move:")
        play1.showboard()


def if_continue(answer, connectionSocket, play1):
    """
    Checks whether the player want to play again the game
    and send the result to player2.

    Args:
        anwer: the anwer of whether to keep playing.
        connectionSocket: the socket object created to make a connection
        play1: a variable with the type BoardClass represents the information of player1

    Returns:
        True if the answer is y or Y.
        False if the answer if n or N.
        'try again' if the answer is none of the above

    """
    if answer == "y" or answer == "Y":
        connectionSocket.send("Play Again".encode())
        return True
    if answer == "n" or answer == "N":
        connectionSocket.send("Fun Times".encode())
        connectionSocket.close()
        play1.printStats()
        return False
    else:
        print("Please enter a valid answer")
        return "try again"


def try_again(answer, connectionSocket):
    """
    Asks user if they want to try again when the connection cannot be made.

    Args:
        anwer: the anwer of whether to try again connecting.
        connectionSocket: the socket object created to make a connection

    Returns:
        True if the answer is y.
        False if the answer if n and close the socket.
        'try again' if the answer is none of the two.

    """
    if answer == "y":
        return True
    if answer == "n":
        connectionSocket.close()
        return False
    else:
        print("Please enter a valid answer")
        return "try again"


def main():
    """
    The main function.
    """

    again = True
    while again:
        try:
            serverAddress = str(input("Enter the host name of player2:\n"))
            serverPort = int(input("Enter the port to use:\n"))

            connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connectionSocket.connect((serverAddress, serverPort))

            # the user name of player 1
            user_name_1 = str(input("Enter the user name of player1:\n"))
            while not user_name_1.isalnum():
                print("Please enter a valid user name.")
                user_name_1 = str(input("Enter the user name of player1:\n"))
            connectionSocket.send(user_name_1.encode())
            
            user_name_2 = connectionSocket.recv(1024).decode("ascii") # the received user name of player2
            if user_name_2: # True if the user name of player2 is received successfully
                print(f"Receive player 2's username: {user_name_2}")
                play1 = BoardClass(user_name_1, user_name_2)

                C = True
                while C:

                    play1.resetGameBoard()

                    playboard(play1, connectionSocket, user_name_1)

                    C = if_continue(str(input("Play again?(Y/N):\n")), connectionSocket, play1)
                    while C == "try again":
                        C = if_continue(str(input("Play again?(Y/N):\n")), connectionSocket, play1)

            again = False

        except Exception:
            again = try_again(str(input("Whether to try again?(y/n)\n")), connectionSocket)
            while again == "try again":
                again = try_again(str(input("Whether to try again?(y/n)\n")), connectionSocket)


if __name__ == '__main__':
    main()
