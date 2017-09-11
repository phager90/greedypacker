"""
    2D Item class.
"""
class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, x, y) -> None:
        self.x = x if x > y else y
        self.y = y if y < x else x
        self.CornerPoint = (0, 0)


    def __repr__(self):
        return 'Item(x=%r, y=%r, CornerPoint=%r)' % (self.x, self.y, self.CornerPoint)


    def rotate(self) -> None:
        self.x, self.y = self.y, self.x


    def area(self) -> int:
        return self.x * self.y
    def __lt__(self, other: 'Item') -> bool:
        return True if self.y < other.y else False


    def __le__(self, other: 'Item') -> bool:
        return True if self.y <= other.y else False


    def __eq__(self, other: 'Item') -> bool:
        return True if self.y == other.y else False


    def __ne__(self, other: 'Item') -> bool:
        return True if self.y != other.y else False


    def __gt__(self, other: 'Item') -> bool:
        return True if self.y > other.y else False


    def __ge__(self, other: 'Item') -> bool:
        return True if self.y >= other.y else False

