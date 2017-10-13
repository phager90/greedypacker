#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""
from functools import reduce
from typing import List
from . import item


class Shelf:
    """
    Shelf class represents of row of items on the sheet
    """
    def __init__(self, x: int, y: int, v_offset: int = 0) -> None:
        self.y = y
        self.x = x
        self.available_width = self.x
        self.vertical_offset = v_offset
        self.items = [] # type: List[item.Item]


    def __repr__(self):
        return str(self.__dict__)
        #return "Shelf(Available Width=%r, Height=%r, Vertical Offset=%r)" % (self.available_width, self.y, self.vertical_offset)


    def insert(self, item: item.Item) -> bool:
        if item.x <= self.available_width and item.y <= self.y:
            item.CornerPoint = (self.x - self.available_width, self.vertical_offset)
            self.items.append(item)
            self.available_width -= item.x
            return True
        return False


class Sheet:
    """
    Sheet class represents a sheet of material to be subdivided.
    Sheets hold a list of rows which hold a list of items.
    """
    def __init__(self, x: int, y: int, rotation: bool = True) -> None:
        self.x = x
        self.y = y
        self.available_height = self.y
        self.shelves = [] # type: List[Shelf]
        self.items = [] # type: List[item.Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Sheet(width=%s, height=%s, shelves=%s)" % (self.x, self.y, str(self.shelves))


    def create_shelf(self, item: item.Item) -> bool:
        if (self.rotation and item.y > item.x and
           item.y < self.x and item.x < self.y):
            item.rotate()
        if item.y <= self.available_height:
            v_offset = self.y - self.available_height
            new_shelf = Shelf(self.x, item.y, v_offset)
            self.shelves.append(new_shelf)
            self.available_height -= new_shelf.y
            new_shelf.insert(item)
            self.items.append(item)
            return True
        return False


    @staticmethod
    def item_fits_shelf(item: item.Item, shelf: Shelf) -> bool:
        if ((item.x <= shelf.available_width and item.y <= shelf.y) or
           (item.y <= shelf.available_width and item.x <= shelf.y)):
            return True
        return False


    @staticmethod
    def rotate_to_shelf(item: item.Item, shelf: Shelf) -> bool:
        """
        Rotate item to long side vertical if that orientation
        fits the shelf.
        """
        if (item.x > item.y and
            item.x <= shelf.y and
            item.y <= shelf.available_width):
            item.rotate()
            return True
        return False


    def add_to_shelf(self, item: item.Item, shelf: Shelf) -> bool:
        if not self.item_fits_shelf(item, shelf):
            return False
        if self.rotation:
            self.rotate_to_shelf(item, shelf)
        res = shelf.insert(item)
        if res:
            self.items.append(item)
            return True
        return False


    def next_fit(self, item: item.Item) -> bool:
        open_shelf = self.shelves[-1]
        if self.item_fits_shelf(item, open_shelf):
            self.add_to_shelf(item, open_shelf)
            return True
        return False


    def first_fit(self, item: item.Item) -> bool:
        for shelf in self.shelves:
            if self.item_fits_shelf(item, shelf):
                self.add_to_shelf(item, shelf)
                return True
        return False


    def best_width_fit(self, item: item.Item) -> bool:
        best_shelf = None
        best_width = float('inf')
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.available_width - item.x < best_width:
                    best_width = shelf.available_width - item.x
                    best_shelf = shelf
        if best_shelf:
            self.add_to_shelf(item, best_shelf)
            return True
        return False


    def best_height_fit(self, item: item.Item) -> bool:
        best_shelf = None
        best_height = float('inf')
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.y - item.y < best_width:
                    best_width = shelf.available_width - item.y
                    best_shelf = shelf
        if best_shelf:
            self.add_to_shelf(item, best_shelf)
            return True
        return False


    def best_area_fit(self, item: item.Item) -> bool:
        best_shelf = None
        best_area = float('inf')
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                remainder_area = (shelf.available_width - item.x)*shelf.y
                if remainder_area < best_area:
                    best_area = remainder_area
                    best_shelf = shelf
        if best_shelf:
            self.add_to_shelf(item, best_shelf)
            return True
        return False


    def worst_width_fit(self, item: item.Item) -> bool:
        worst_shelf = None
        worst_width = 0
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.available_width - item.x > worst_width:
                    worst_width = shelf.available_width - item.x
                    worst_shelf = shelf
        if worst_shelf:
            self.add_to_shelf(item, worst_shelf)
            return True
        return False


    def worst_height_fit(self, item: item.Item) -> bool:
        worst_shelf = None
        worst_height = 0
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.y - item.x > worst_height:
                    worst_height = shelf.available_width - item.x
                    worst_shelf = shelf
        if worst_shelf:
            self.add_to_shelf(item, worst_shelf)
            return True
        return False


    def worst_area_fit(self, item) -> bool:
        worst_shelf = None
        worst_area = 0
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                remainder_area = (shelf.available_width - item.x)*shelf.y
                if remainder_area > worst_area:
                    worst_area = remainder_area
                    worst_shelf = shelf
        if worst_shelf:
            self.add_to_shelf(item, worst_shelf)
            return True
        return False


    def insert(self, item: item.Item, heuristic: 'str' = 'next_fit') -> bool:
        if (item.x <= self.x and item.y <= self.y):
            # First Item Insert
            if not self.shelves:
                return self.create_shelf(item)

            heuristics = {'next_fit': self.next_fit,
                          'first_fit': self.first_fit,
                          'best_width_fit': self.best_width_fit,
                          'best_height_fit': self.best_height_fit,
                          'best_area_fit': self.best_area_fit,
                          'worst_width_fit': self.worst_width_fit,
                          'worst_height_fit': self.worst_height_fit,
                          'worst_area_fit': self.worst_area_fit }

            if heuristic in heuristics:
                # Call Heuristic
                res = heuristics[heuristic](item)
                # If item inserted successfully
                if res:
                    return True
            # No shelf fit
            return self.create_shelf(item)
        # No sheet fit
        return False


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """

        stats = {
            'width': self.x,
            'height': self.y,
            'area': self.x * self.y,
            'efficiency': sum([i.x*i.y for i in self.items])/(self.x*self.y),
            'items': self.items,
            }

        return stats

if __name__ == '__main__':
    SHEET = Sheet(8, 5)
    ITEM = item.Item(2, 6)
    ITEM2 = item.Item(3, 2)
    ITEM3 = item.Item(1, 1)
    ITEM4 = item.Item(4, 2)
    ITEM5 = item.Item(1, 8)
    SHEET.insert(ITEM, heuristic='worst_width_fit')
    SHEET.insert(ITEM2, heuristic='worst_width_fit')
    SHEET.insert(ITEM3, heuristic='worst_width_fit')
    SHEET.insert(ITEM4, heuristic='worst_width_fit')
    SHEET.insert(ITEM5, heuristic='worst_width_fit')
    print(SHEET)
    print()
    for i, shelf in enumerate(SHEET.shelves):
        print('Shelf #%s: %r' % (i, str(shelf.items)))
    print()
    print(SHEET.bin_stats())