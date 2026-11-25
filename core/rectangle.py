class Rectangle:
    """
    A class representing a rectangle initialized with length: int and width: int.

    Requirements:
    - Initialized with length: int and width: int.
    - Validates both dimensions are integers, strictly rejecting booleans, floats, strings, etc.
    - Iterable: yields {'length': self.length} first, followed by {'width': self.width}.
    - Supports multiple iterations over the same instance cleanly.
    """

    def __init__(self, length: int, width: int):
        # type(x) is not int strictly rejects booleans, floats, strings, None, etc.
        # Note: In Python, bool subclasses int (isinstance(True, int) is True),
        # so type(val) is not int or (isinstance(val, int) and not isinstance(val, bool)) is required.
        if type(length) is not int:
            raise TypeError(f"length must be an integer, got {type(length).__name__}")
        if type(width) is not int:
            raise TypeError(f"width must be an integer, got {type(width).__name__}")

        self.length = length
        self.width = width

    def __iter__(self):
        """
        Generator yielding the dimensions in the required format:
        1. {'length': <length>}
        2. {'width': <width>}
        """
        yield {'length': self.length}
        yield {'width': self.width}

    def __repr__(self):
        return f"Rectangle(length={self.length}, width={self.width})"

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return False
        return self.length == other.length and self.width == other.width

