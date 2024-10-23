from cmath import cos, sin

import pygame as game

from App import *
from VerletPhysics import *


class DemoRope(App):
    #
    world = World(Vector(1000.0, 900.0), Vector(0, 2), 4)
    #
    grabbed = None
    radius = 20
    strength = 0.20

    #
    def Initialize(self):
        rope = self.world.AddComposite()
        particles = list()
        j = 0
        for i in range(0, 50):
            particles.append(self.world.AddParticle(self.world.hsize.x, 10.0 + j))
            j += 15
        rope.AddParticles(*particles)
        constraints = list()
        for i in range(0, 49):
            constraints.append(self.world.AddConstraint(rope.particles[i], rope.particles[i+1], 1.0))
        rope.AddConstraints(*constraints)
        rope.particles[0].material.mass = 0.0
 #       rope.particles[49].ApplyForce(Vector(-cos(self.world.delta), 0))

    #
    def Update(self):
        #
        if game.mouse.get_pressed()[0]:
            if self.grabbed == None:
                closest = self.ClosestPoint()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed != None:
                mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
                force = (mouse - self.grabbed.position) * self.strength
                print(force)
                self.grabbed.ApplyImpulse(force)
        else:
            self.grabbed = None
        #
        if game.key.get_pressed()[game.K_ESCAPE]:
            self.Exit()
        self.world.Simulate(self.t)

    #
    def Render(self):
        #
        self.screen.fill((24, 24, 24))
        for c in self.world.constraints:
            pos1 = (int(c.node1.position.x), int(c.node1.position.y))
            pos2 = (int(c.node2.position.x), int(c.node2.position.y))
            game.draw.line(self.screen, (0, 255, 0), pos1, pos2, 3)
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 255, 255), pos, 5, 0)
        game.display.update()

    def ClosestPoint(self):
        mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        closest = None
        distance = float('inf')
        for particle in self.world.particles:
            d = mouse.distance(particle.position)
            if d < distance:
                closest = particle
                distance = d
        return (closest, distance)


if __name__ == "__main__":
    app = DemoRope("Application", 1000, 900, 60)
    app.Run()
