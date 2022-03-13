import math


class vec2d(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return vec2d(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return vec2d(self.x - other.x, self.y - other.y)

    def mul(self, other):
        return vec2d(self.x*other.x, self.y*other.y)

    def abs(self):
        return math.sqrt(self.x**2 + self.y**2)

    def eq(self, other):
        return self.x == other.x and self.y == other.y

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def str(self):
        return '(%g, %g)' % (self.x, self.y)

    def displaystr(self):
        if abs(self.y) < 0.01:
            self.y = 0
        return '(%.2f, %.2f)' % (self.x, -self.y)

    def ne(self, other):
        return not self.eq(other)

    def mag(self):
        x = int(self.x)
        y = int(self.y)
        return math.sqrt(x ** 2 + y ** 2)

    def getpgpos(self):
        return self.x, self.y

    def setmag(self, val):
        x = self.x; y = self.y
        mag = self.mag()
        if mag != 0:
            x *= val/mag
            y *= val/mag
        else:
            return vec2d(0, 0)
        return vec2d(x, y)

    def normal(self):
        return vec2d(self.y, -self.x)

    def normalized(self):
        return self.setmag(1)

    def scale(self, factor):
        return vec2d(self.x * factor, self.y * factor)

    def limit(self, max):

        if self.mag() > max:
            return self.setmag(max)
        else:
            return self
