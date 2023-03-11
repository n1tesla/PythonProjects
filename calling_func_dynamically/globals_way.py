import math

class Rectangle:
    length: int
    width: int

    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def do_area(self):
        area = self.length * self.width
        print(f"The area of the rectangle is: {area}")

    def do_perimeter(self):
        perimeter = (self.length + self.width) * 2
        print(f"The perimeter of the rectangle is: {perimeter}")

    def do_diagonal(self):
        diagonal = math.sqrt(self.length ** 2 + self.width ** 2)
        print(f"The diagonal of the rectangle is: {diagonal}")




    def solve_for(self, name: str, *args, **kwargs):
        do = f"get_{name}"
        if hasattr(self, do) and callable(func := getattr(self, do)):
            func(*args, **kwargs)


rectangle = Rectangle(3, 5)

rectangle.solve_for('area')
rectangle.solve_for('perimeter')
rectangle.solve_for('diagonal')


