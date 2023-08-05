from typing import Union, Iterator, Dict, Hashable

class GameState():
    def get_current_team(self) -> Union[int,str]:
        """The identifier of the current player's team."""
        raise NotImplementedError("GameState must implement get_current_team.")

    def get_legal_moves(self, randomize:bool=False) -> Iterator[Hashable]:
        """An iterator of all legal moves in this state.
        The randomize param instructs the method to yield moves in a random order.
        """
        raise NotImplementedError("GameState must implement get_legal_moves.")

    def get_random_move(self) -> Hashable:
        """Returns a random legal move from this state."""
        return next(self.get_legal_moves(True))

    def has_move(self) -> bool:
        """Returns whether there are any legal moves in this state."""
        try:
            next(self.get_legal_moves())
            return True
        except StopIteration:
            return False

    def make_move(self, move:Hashable) -> 'GameState':
        """Returns a new GameState, which is the result of applying the given move to this state.
        This usually involves updating the board and advancing the player counter.
        The current state object (self) should not be modified. Rather, modify a copy of it.
        """
        raise NotImplementedError("GameState must implement make_move.")

    def is_terminal(self) -> bool:
        """Checks if the game is over."""
        raise NotImplementedError("GameState must implement is_terminal.")

    def get_reward(self) -> Union[float, Dict[Union[int,str], float]]:
        """Returns the reward earned by the team that played the game-ending move.
        Typically 1 for win, -1 for loss, 0 for draw.
        Alternatively, returns a dict of format {team:reward} or {team1:reward1, team2:reward2, ...}
        Note: This method is only evaluated on terminal states.
        """
        raise NotImplementedError("GameState must implement get_reward.")

    def __hash__(self) -> int:
        raise NotImplementedError("GameState must implement __hash__")

    def __eq__(self, other:'GameState') -> bool:
        raise NotImplementedError("GameStates must implement __eq__")
