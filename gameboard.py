class BoardClass:
    """ Operate the game board.

    The class contains, updates, and shows all the information of
    the two players and the board.

    Attributes:
        player: players user name(str).
        lastplayer: user name of the last player to have a turn(str).
        wins: number of wins(int).
        ties: number of ties(int).
        losses: number of losses(int).
        board: the game board with players' move.
        games: the total number of games played.
        move: all the moves made by two players

    """
    def __init__(self,  player: str = "", lastplayer: str = "", wins: int= 0, ties: int = 0, losses: int = 0, board: list = [], games: int = 0, move: list = []) -> None:
        """
        Set up the initializations.

        Args:
            player: Players user name.
            lastplayer: User name of the last player to have a turn.    
            wins: Number of wins.
            ties: Number of ties.
            losses:Number of losses.
            board: the game board with players' move.
            games: Number of total games.
            move: each move.

        """
        self.player = player
        self.lastplayer = lastplayer
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.board = [[" "]*3, [" "]*3, [" "]*3]
        self.games = games
        self.move = []


    def updateGamesPlayed(self):
        """
        Keeps track how many games have started.

        """
        self.games += 1


    def resetGameBoard(self):
        """
        Resets the game board and clears all the moves.

        """
        self.board = [[" "]*3, [" "]*3, [" "]*3]
        self.move = []


    def player1or2(self):
        """
        Checks current player is player1 or player2.

        Returns:
            1: the current player is player1.
            2: the current player is player2.

        """
        if self.player == "player2":
            return 2
        else:
            return 1


    def movevalid(self, move):
        """
        Checks if the move entered is valid or not.

        Args:
            move: the move maded by the player.

        Returns:
            True: the move is valid.
            False: the move is invalid

        """
        try:
            move = int(move)
            move = str(move)
            if move in self.move:
                print("The place is already be taken.")
                return False
            if len(move) == 2:
                if int(move[0]) in [1,2,3] and int(move[1]) in [1,2,3]:
                    return True
                else:
                    print("The move is out of range.")
                    return False
            else:
                print("Please an valid move following the instruction.")
                return False
        except:
            print("Please an valid move following the instruction.")
            return False


    def updateGameBoard(self, currentplayer, move):
        """
        Updates the game board.

        Args:
            currentplayer: the player who is making the move.
            move: the move maded by the player.

        """  
        move = str(move)
        row = int(move[0])-1
        col = int(move[1])-1
        if currentplayer == "player2":
            self.board[row][col] = "O"
        else:
            self.board[row][col] = "X"
        self.move.append(move)
        self.lastplayer = currentplayer
        

    def isWinner(self):
        """
        Checks if the latest move resulted in a win
        and updates the wins and losses count.

        Returns:
            True: someone wins the game.
            False: no one wins the game yet.

        """
        if self.move:
            row = int(self.move[-1][0])-1
            col = int(self.move[-1][1])-1
            XorO = self.board[row][col]
            boardrow = all(element == XorO for element in self.board[row])
            boardcol = all(element == XorO for element in [self.board[0][col],self.board[1][col],self.board[2][col]])
            boardcross1 = all(element == XorO for element in [self.board[0][0],self.board[1][1],self.board[2][2]])
            boardcross2 = all(element == XorO for element in [self.board[0][2],self.board[1][1],self.board[2][0]])
            if boardrow or boardcol or boardcross1 or boardcross2:
                if (self.player1or2() == 1 and XorO == "X") or (self.player1or2() == 2 and XorO == "O"):
                    self.wins += 1
                else:
                    self.losses += 1
                self.updateGamesPlayed()
                return True
            else:
                return False
        else:
            return False

 

    def boardIsFull(self):
        """
        Checks if the board is full and updates the ties count.

        Returns:
            True: if the board is full.
            False: the board is not full.
        """
        if all(" " not in element for element in self.board):
            self.updateGamesPlayed()
            self.ties += 1
            return True
        else:
            return False


    def printStats(self):
        """
        Prints the information of players user name, the user name of the last person to make a move,
        number of games, the number of wins, the number of losses, the number of ties.
        """
        print(f"The players user name: {self.player}")
        print(f"The user name of the last person to make a move: {self.lastplayer}")
        print(f"The number of games: {self.games}")
        print(f"The number of wins: {self.wins}")
        print(f"The number of losses: {self.losses}")
        print(f"The number of ties: {self.ties}")
        
    def showboard(self):
        """
        Presents the current board state to players after each player makes a move.
        """
        print(self.board[0])
        print(self.board[1])
        print(self.board[2])

    def gameover(self):
        """
        Checks whether the game is over: the game is over when there is a winner or the board if full.

        Returns:
            True: the game is over as the board is full or someone has winned the game.
            False: the game is not over.
        """
        if self.isWinner() == False and self.boardIsFull() == False:
            return False
        else:
            return True



        



        
    
