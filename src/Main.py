from cmath import cos, sin
import pygame as game
from App import *
from VerletPhysics import *


class DemoRope(App):
    world = World(Vector(1000.0, 2500.0), Vector(0, 2), 4)
    grabbed = None
    radius = 20
    strength = 0.20
    scale = 1.0
    offset = Vector(0, 0)

    def Initialize(self):
        rope = self.world.AddComposite()
        particles = list()
        j = 0

        for i in range(0, 100):
            particle = self.world.AddParticle(self.world.hsize.x, 10.0 + j)
            particle.velocity = Vector(0, 0)
            particles.append(particle)
            j += 15
        rope.AddParticles(*particles)

        constraints = list()

        for i in range(0, 99):
            constraints.append(self.world.AddConstraint(rope.particles[i], rope.particles[i + 1], 1.0))
        rope.AddConstraints(*constraints)

        rope.particles[0].material.mass = 0.0

    def Update(self):
        keys = game.key.get_pressed()

        if keys[game.K_EQUALS] or keys[game.K_KP_PLUS]:
            self.scale *= 1.1
            self.AdjustOffset()
        if keys[game.K_MINUS] or keys[game.K_KP_MINUS]:
            self.scale /= 1.1
            self.AdjustOffset()
        if keys[game.K_UP]:
            self.offset.y += 10
        if keys[game.K_DOWN]:
            self.offset.y -= 10

        if game.mouse.get_pressed()[0]:
            if self.grabbed == None:
                closest = self.ClosestPoint()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed != None:
                mouse = Vector((game.mouse.get_pos()[0] - self.offset.x) / self.scale,
                               (game.mouse.get_pos()[1] - self.offset.y) / self.scale)
                force = (mouse - self.grabbed.position) * self.strength
                self.grabbed.ApplyImpulse(force)
        else:
            self.grabbed = None

        if keys[game.K_ESCAPE]:
            self.Exit()

        self.world.Simulate(self.t)

    def Render(self):
        self.screen.fill((24, 24, 24))
        for c in self.world.constraints:
            pos1 = (
            int(c.node1.position.x * self.scale + self.offset.x), int(c.node1.position.y * self.scale + self.offset.y))
            pos2 = (
            int(c.node2.position.x * self.scale + self.offset.x), int(c.node2.position.y * self.scale + self.offset.y))
            game.draw.line(self.screen, (0, 255, 0), pos1, pos2, 3)
        for p in self.world.particles:
            pos = (int(p.position.x * self.scale + self.offset.x), int(p.position.y * self.scale + self.offset.y))
            game.draw.circle(self.screen, (255, 255, 255), pos, int(5 * self.scale), 0)
        game.display.update()

    def ClosestPoint(self):
        mouse = Vector((game.mouse.get_pos()[0] - self.offset.x) / self.scale,
                       (game.mouse.get_pos()[1] - self.offset.y) / self.scale)
        closest = None
        distance = float('inf')
        for particle in self.world.particles:
            d = mouse.distance(particle.position)
            if d < distance:
                closest = particle
                distance = d
        return (closest, distance)

    def AdjustOffset(self):
        screen_width, screen_height = self.screen.get_size()
        world_center_x = self.world.hsize.x * self.scale
        world_center_y = self.world.hsize.y * self.scale
        self.offset.x = screen_width / 2 - world_center_x
        self.offset.y = screen_height / 2 - world_center_y


if __name__ == "__main__":
    app = DemoRope("Application", 1000, 900, 60)
    app.Run()