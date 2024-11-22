class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def set_width(self, width):
        self._width = width
    
    def set_height(self, height):
        self._height = height
    
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def area(self):
        return self._width * self._height

class Square(Rectangle):
    def __init__(self, side):
        self._width = side
        self._height = side
    
    def set_width(self, width):
        self._width = width
        self._height = width
    
    def set_height(self, height):
        self.set_width(height)


def resize_rectangle(rectangle):
    rectangle.set_width(10)
    rectangle.set_height(20)
    assert rectangle.area() == 200, "Area calculation is incorrect!"


if __name__ == '__main__':
    rect = Rectangle(4, 4)
    print(f"Area of rectangle: {rect.area()}")
    resize_rectangle(rect)

    rect = Square(4)
    print(f"Area of square: {rect.area()}")
    resize_rectangle(rect)

