import pygame as pg
import pygame.gfxdraw
from vec2d import vec2d as vec
from shape import Shape
from random import randint


class CollisionMaster:
    def __init__(self):
        self.width = 1200
        self.height = 1000
        self.fps = 60
        self.clock = pg.time.Clock()
        self.windowname = pg.display.set_caption("Collisions : - )")
        self.surface = pg.display.set_mode((self.width, self.height))
        self.shapelist = []
        self.grav = 0.5
        self.acc = vec(0, 0)
        pg.font.init()
        self.font = pg.font.SysFont("Luckiest Guy", 10)
        self.mouse_velocity = vec(0, 0)
        self.dragvalue = -1
        self.initialv = vec(0, 0)
        self.e = 0.2
        self.showv = 0

    def setgrav(self, grav):
        self.grav = grav

    def makeScene(self, width, height):
        self.width = width
        self.height = height
        self.surface = pg.display.set_mode((self.width, self.height))
        self.loop()

    def add(self, sh):
        self.shapelist.append(sh)
        sh.acc = vec(0, self.grav)

    def updateshapes(self):
        for shape in self.shapelist:
            shape.update(self.width, self.height)

    def circledetection(self):
        circle_list = []
        for sh in self.shapelist:
            if sh.shape == "circle":
                circle_list.append(sh)

        for i in range(len(circle_list)):
            for j in range(i + 1, len(circle_list)):
                circ1 = circle_list[i]
                circ2 = circle_list[j]
                # if circ1.name == circ2.name:
                #     continue
                if self.colliding(circ1, circ2):
                    pygame.draw.line(self.surface, (255, 0, 0), circ1.get_tuple_pos(), circ2.get_tuple_pos())
                    try:
                        delta = circ1.pos.sub(circ2.pos)
                        d = delta.mag()
                        mtd = delta.scale((circ1.size + circ2.size - d) / d)
                    except ZeroDivisionError:
                        circ1.pos = circ1.pos.add(vec(0, 1))
                        delta = circ1.pos.sub(circ2.pos)
                        d = delta.mag()
                        mtd = delta.scale((circ1.size + circ2.size - d) / d)

                    im1 = 1 / circ1.size
                    im2 = 1 / circ2.size

                    circ1.pos = circ1.pos.add(mtd.scale(im1 / (im1 + im2)))
                    circ2.pos = circ2.pos.sub(mtd.scale(im2 / (im1 + im2)))

                    v = circ1.vel.sub(circ2.vel)
                    vn = v.dot(mtd.normalized())

                    if vn > 0:
                        return

                    self.e = 0.05
                    li = (-(1 + self.e) * vn) / (im1 + im2)
                    impulse = mtd.normalized().scale(li)

                    circ1.vel = circ1.vel.add(impulse.scale(im1))
                    circ2.vel = circ2.vel.sub(impulse.scale(im2))

    @staticmethod
    def colliding(c1, c2):
        if (c1.pos.sub(c2.pos)).mag() <= c1.size +  c2.size:
            return 1

    @staticmethod
    def randcolor():
        return randint(0, 255), randint(0, 255), randint(0, 255)

    def drawshapes(self):
        polygons = ["square", "triangle"]
        for sh in self.shapelist:
            if sh.shape in polygons:
                pg.gfxdraw.aapolygon(self.surface, sh.points, sh.color)
                pg.gfxdraw.filled_polygon(self.surface, sh.points, sh.color)

            elif sh.shape == "circle":
                pg.gfxdraw.filled_circle(self.surface, sh.get_tuple_pos()[0], sh.get_tuple_pos()[1], sh.size, sh.color)
                pg.gfxdraw.aacircle(self.surface, sh.get_tuple_pos()[0], sh.get_tuple_pos()[1], sh.size, sh.color)

    def applygravity(self):
        for shape in self.shapelist:
            shape.acc = vec(0, self.grav)

    def showvelocities(self):
        for shape in self.shapelist:
            pg.draw.line(self.surface, (255, 50, 50), shape.pos.getpgpos(),
                         shape.pos.add(shape.vel.scale(4)).getpgpos(), 5)

            vel_text = shape.vel.displaystr()
            self.font = pg.font.SysFont("Luckiest Guy", int(shape.size/2))
            text = self.font.render(vel_text, 1, shape.color)
            size = self.font.size(vel_text)
            self.surface.blit(text, (shape.pos.x - size[0]/2, shape.pos.y - shape.size - size[1]))

    def printKE(self):
        KE = 0
        PE = 0
        for shape in self.shapelist:
            KE += .5 * shape.size * shape.vel.mag()**2
            PE += shape.size * (self.height - shape.pos.y - shape.size)
        KE = round(KE, 2)
        PE = round(PE, 2)
        print(KE, PE, KE + PE)

    def drag_and_drop(self, clicked, lastclick, vel, pos):

        if clicked:
            for i in range(len(self.shapelist)):
                shape = self.shapelist[i]
                if shape.pos.sub(pos).mag() <= shape.size:
                    shape.pos = pos
                    shape.vel = vec(0, 0)
                    shape.acc = vec(0, 0)
                self.dragvalue = i
        if lastclick and not clicked:
            try:
                concerned_shape = self.shapelist[self.dragvalue]
                concerned_shape.vel = vel
                concerned_shape.acc = vec(0, self.grav)
            except IndexError:
                pass

    def loop(self):
        currentpos = (0, 0)
        posvec = vec(400, 400)
        clicked = 0
        while True:
            self.clock.tick(self.fps)
            self.surface.fill((0, 0, 0))

            self.updateshapes()
            self.circledetection()
            self.drawshapes()
            self.events()
            postuple = pg.mouse.get_pos()

            lastpos = posvec
            posvec = vec(postuple[0], postuple[1])
            lastclick = clicked
            clicked = pg.mouse.get_pressed()[0]
            cursorvel = posvec.sub(lastpos).scale(.25)
            self.initialv = cursorvel
            self.drag_and_drop(clicked, lastclick, cursorvel, posvec)
            if self.showv:
                self.showvelocities()

            #self.printKE()
            pg.display.update()

    def events(self):
        for event in pg.event.get():
            keys = pg.key.get_pressed()

            if keys[pg.K_x]:
                self.shapelist.clear()
            if keys[pg.K_v]:
                if self.showv:
                    self.showv = 0
                else:
                    self.showv = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pg.K_c:
                    pos = pygame.mouse.get_pos()
                    vecpos = vec(pos[0], pos[1])
                    self.add(Shape("circle", randint(40, 60), vecpos,
                                   self.randcolor(), "ball", initialv=self.initialv, frict=0.000))

                if event.key == pg.K_f:

                    if self.fps == 60:
                        self.fps = 1
                    else:
                        self.fps = 60
            if event.type == pg.QUIT:
                quit()

