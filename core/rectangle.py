class Rectangle:
    def __init__(self, length: int, width: int):
        # In Python bool subclasses int (isinstance(True, int) is True),
        # so check type explicitly to disallow booleans.
        if type(length) is not int:
            raise TypeError("length must be an integer")
        if type(width) is not int:
            raise TypeError("width must be an integer")

        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

    def __repr__(self):
        return f"Rectangle(length={self.length}, width={self.width})"
