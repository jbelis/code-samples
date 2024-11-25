class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement area")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self._width = width
    
    def set_height(self, height):
        self._height = height
    
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
 
    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def get_side(self):
        return self._width
    
    def set_side(self):
        return self._height

    def area(self):
        return self.side ** 2


if __name__ == '__main__':
    rect = Rectangle(4, 4)
    print(f"Area of rectangle: {rect.area()}")
    resize_rectangle(rect)

    rect = Square(4)
    print(f"Area of square: {rect.area()}")
    resize_rectangle(rect)




# Demonstrates correct usage
def correct_shape_usage():
    shapes = [
        Rectangle(4, 5),
        Square(4)
    ]
    
    # Each shape can be used interchangeably
    for shape in shapes:
        print(f"Shape area: {shape.area()}")


