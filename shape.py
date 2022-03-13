from vec2d import vec2d as vec


class Shape:
    def __init__(self, shape, size, pos, color, name, initialv=vec(0, 0), acc=vec(0, 0), frict=0):
        self.shape = shape
        self.size = size
        self.pos = pos
        self.color = color
        self.points = []
        self.name = name
        self.initialv = initialv
        self.vel = self.initialv
        self.acc = acc
        self.frict = frict
        self.setpoints()

    def setpoints(self):
        if self.shape == "square":
            self.points = [(self.pos.x, self.pos.y),
                           (self.pos.x + self.size, self.pos.y),
                           (self.pos.x + self.size, self.pos.y + self.size),
                           (self.pos.x, self.pos.y + self.size)]

        if self.shape == "triangle":
            self.points = [(self.pos.x + self.size/2, self.pos.y + self.size*0.866),
                           (self.pos.x, self.pos.y),
                           (self.pos.x + self.size, self.pos.y)]

    def get_tuple_pos(self):
        return int(self.pos.x), int(self.pos.y)

    def update(self, width, height):

        self.pos = self.pos.add(self.vel)

        if self.pos.y + self.size >= height:
            self.vel.y *= -1
            self.pos.y = height - self.size + self.acc.y
        elif self.pos.y - self.size <= 0:
            self.pos.y = self.size - self.acc.y
            self.vel.y *= -1
        else:
            self.vel.y += self.acc.y

        if self.pos.x + self.size >= width:
            self.pos.x = width - self.size + self.acc.x
            self.vel.x *= -1
        elif self.pos.x - self.size <= 0:
            self.pos.x = self.size - self.acc.x
            self.vel.x *= -1
        else:
            self.vel.x += self.acc.x

        self.vel = self.vel.scale(1-self.frict)
        self.setpoints()
