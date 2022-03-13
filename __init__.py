from collision_master import CollisionMaster as coll
from shape import Shape
from vec2d import vec2d as vec

scene = coll()
scene.setgrav(0.2)
# x = Shape("circle", 50, vec(400, 300), (50, 255, 50), "dodo", initialv=vec(5, -2), frict=0.000)
# x3 = Shape("circle", 50, vec(400, 450), (50, 50, 200), "dofo", initialv=vec(4, 0), frict=0.000)
# scene.add(x3)
# scene.add(x)
scene.makeScene(1200, 1000)


