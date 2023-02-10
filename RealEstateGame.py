# Author: Behrad Noorani
# GitHub username: Hyouketsu
# Description: Simple monopoly clone game called RealEstateGame that can be played using code, uses concepts of OOP 


class RealEstateGame:
    """
    the main realstategame object that creates the game and all its variables
    it is responsible for communicating with other (space and player) objects of
    this game and includes the main methods of the game such as moving which it
    communicates with those mentioned objects
    """
    def __init__(self):
        """initializes the RealEstateGame with empty lists of player and spaces"""
        self._players = []
        self._spaces = []
        self._go = None

    def create_spaces(self, start, rent_amounts):
        """
        start: the amount collected for passing the GO space
        rent_amounts: array of ints representing the rent amount of each space
        creates space class objects and appends them to the list of spaces, also creates the go spaces
        at pos 0. also assigns a value to the GO bonus
        """
        self._go = start
        self._spaces.append(Space(0, 0))
        for position in self._spaces:
            if 0 == position.get_pos():
                position.set_owner("game")
        counter = 1
        for rent in rent_amounts:
            self._spaces.append(Space(counter, rent))
            counter += 1

    def create_player(self, name, start_bal):
        """
        name: name of the player to be created
        start_bal: starting balance of the player object being created
        creates player class objects and appends them to the list players
        """
        self._players.append(Player(name, start_bal))

    def get_player_account_balance(self, name):
        """
        name: name of the player
        returns the account balance of a specific player by iterating through player object list and communicating with
        the player object
        """
        for player in self._players:
            if player.get_name() == name:
                return player.get_funds()

    def get_player_current_position(self, name):
        """
        name: name of the player
        returns the current position of a specific player by iterating through player object list and communicating with
        the player object
        """
        for player in self._players:
            if player.get_name() == name:
                return player.get_pos()

    def buy_space(self, name):
        """
        name: name of the player
        buys the current pos that the player is in and adds it to their owner position and sets them as the owner of
        said position on the space class
        """
        for player in self._players:
            if player.get_name() == name:
                curr_pos = player.get_pos()
                if self.check_owned(curr_pos) is False:
                    value = self.get_value(curr_pos) * 5
                    if value < player.get_funds():
                        player.buy_pos()
                        player.pay_fund(value)
                        for position in self._spaces:
                            if curr_pos == position.get_pos():
                                position.set_owner(player)
                    else:
                        print("Not enough funds to buy this space")
                else:
                    print("space is already owned")
                    return False

    def move_player(self, name, spaces):
        """
        name: name of the player
        spaces: spaces the player should move
        checks if the resulting move would go over 24 in which case it would reset the position to 0
        If the player's account balance is 0, the method will return immediately without doing anything
        number of spaces moved should be between 1-6
        """
        if spaces > 6 or spaces < 1:
            print("Invalid spaces entered")
        else:
            for player in self._players:
                if player.get_name() == name:
                    curr_pos = player.get_pos()
                    if curr_pos + spaces > 24:
                        player.reset_pos()
                        player.add_fund(self._go)
                        remaining = spaces + curr_pos - 24
                        player.move_pos(remaining - 1)
                    else:
                        player.move_pos(spaces)
                    next_pos = player.get_pos()
                    if self.check_owned(next_pos) is True:
                        self.pay_rent(player, next_pos)

    def check_game_over(self):
        """
        this method will iterate through the
        list of players and checks how many players have an account balance of more than 0. if the count is more than 1,
        this will return an empty string and the game is not over. if the county is 1 then the player with an account
        balance more than 0 is declared as the winner and their name is returned as a string
        """
        player_count = len(self._players)
        counter = 0
        if player_count == 1:
            for player in self._players:
                return player.get_name()
        for player in self._players:
            if player.get_funds == 0:
                counter += 1
        if counter == (player_count - 1):
            for player in self._players:
                if player.get_funds != 0:
                    return player.get_name()
        else:
            return "No one has won the game yet"

    def pay_rent(self, player, pos):
        """
        name: name of the player
        pos: current position of the player used to determine the amount of rent to be paid
        method to pay rent as a result of a move by move_player. the player pays rent if the space is owned
        the player should not pay more than their funds balance
        """
        for space in self._spaces:
            if pos == space.get_pos():
                owner = space.get_owner()
                rent = space.get_rent()

        curr_funds = player.get_funds()
        if curr_funds > rent:
            player.pay_fund(rent)
            owner.add_fund(rent)
        else:
            player.pay_fund(curr_funds)
            owner.add_fund(curr_funds)
            self._players.remove(player)
            player.lost(self.get_space_list())

    def check_owned(self, pos):
        """
        pos: position that is being inspected for being owned
        checks if the position has an owner
        """
        for position in self._spaces:
            if pos == position.get_pos():
                if position.get_owner() is None or position.get_owner() == 0:
                    return False
                else:
                    return True

    def get_value(self, pos):
        """
         pos: position that is being inspected for rent
         returns the rent of a position
        """
        for position in self._spaces:
            if pos == position.get_pos():
                return position.get_rent()

    def get_player_list(self):
        """
        returns the player list of realstategame
        """
        return self._players

    def get_space_list(self):
        """
        returns the space list of realstategame
        """
        return self._spaces


class Player:
    """
    player object representing a player of the realstategame. every player object is init'd with a name and initial
    funds and has a list of owned spaces. each player object also contains the current position of the player.
    """
    def __init__(self, name, funds):
        """
        inits the player class object with the given name and starting funds, sets the owner list t oa na empty list
        and puts the player at position 0
        """
        self._name = name
        self._funds = funds
        self._owner = []
        self._position = 0

    def get_name(self):
        """
        returns the name of the player. used extensively in the realstategame class methods to make changes to the
        player objects
        """
        return self._name

    def get_funds(self):
        """
        returns the current funds of the player used in many methods of the realstategame
        """
        return self._funds

    def get_pos(self):
        """
        returns the current pos of the player. used in the moving method of the realstategame
        """
        return self._position

    def move_pos(self, spaces):
        """
        moves the player by the amount of spaces in the realstategame used in the move method of the realstategame
        """
        self._position += spaces

    def buy_pos(self):
        """
        sets the current pos of the player in the owned spaces list and makes the necessary changes to the Space
        object representing the current pos
        """
        self._owner.append(self._position)

    def add_fund(self, amount):
        """
        adds a certain amount of funds to the current balance of the player used in collecting rent and moving through
        the go space
        """
        self._funds += amount

    def pay_fund(self, amount):
        """
        decducts a certain amount of funds to the current balance of the player
        """
        self._funds -= amount

    def reset_pos(self):
        """
        resets the position of the player to 0 ofr when they pass go
        """
        self._position = 0

    def lost(self, spaces):
        """
        contains the actions needed for setting a player as lost such as resetting the spaces' owner by them to not
        being owned
        """
        for space in spaces:
            if space.get_owner is self:
                space.reset_owner()


class Space:
    """
    represents a space on the board of the realstategame with its rent, position on the board 0-24 and the current owner
    which would be a player clas object
    """
    def __init__(self, pos, rent):
        """
        inits the board space class with the rent amount and its position 1-24 and sets the owner to None
        """
        self._rent = rent
        self._pos = pos
        self._owner = None

    def get_owner(self):
        """
        returns the owner of a space. used in determining if a position is owned or not to determine if it can be
        bought or rent has to be collected
        """
        return self._owner

    def get_rent(self):
        """
        returns the rent amount to be collected from moving to the space.
        """
        return self._rent

    def get_pos(self):
        """
        returns the position of the current space on the board 1-24
        """
        return self._pos

    def reset_owner(self):
        """
        resets the owner of the space object to none. used when a player lost and lost ownership of their owned spaces
        """
        self._owner = None

    def set_owner(self, owner):
        """
        sets the parameter owner as the owner of the space
        """
        self._owner = owner

# game = RealEstateGame()
#
# rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350, 350]
# game.create_spaces(50, rents)
#
# game.create_player("Player 1", 1000)
# game.create_player("Player 2", 1000)
# game.create_player("Player 3", 1000)
#
# game.move_player("Player 1", 6)
# game.buy_space("Player 1")
# game.move_player("Player 2", 6)
#
# print(game.get_player_account_balance("Player 1"))
# print(game.get_player_account_balance("Player 2"))
#
# print(game.check_game_over())
