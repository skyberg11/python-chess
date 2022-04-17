class OutOfRange(Exception):
    """Raised when move is incorrect"""
    pass

class Check(Exception):
    """Raised when move leads to check"""
    pass

class SelfHarm(Exception):
    """Raised when the rule is violated"""
    pass

class LazyMove(Exception):
    """Raised when the player doesnt moves"""
    pass

class IncorrectFigure(Exception):
    """Raised when the player picks bad figure"""
    pass

class IncorrectMove(Exception):
    """Raised when the move is incorrect"""
    pass