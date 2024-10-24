from Vector import *
from Particle import *
from Constraint import *


class Composite:
    particles = list()  # list of particles composing this shape
    constraints = list()  # list of constraints composing this shape

    def __init__(self, *params):
        for param in self.traverse(params):
            if isinstance(param, Particle):
                self.particles.append(param)
            elif isinstance(param, Constraint):
                self.constraints.append(param)
            print(len(self.particles))

    def AddParticles(self, *particles):
        for particle in particles:
            if isinstance(particle, Particle):
                self.particles.append(particle)

    def AddConstraints(self, *constraints):
        for constraint in constraints:
            if isinstance(constraint, Constraint):
                self.constraints.append(constraint)

    def SetMaterial(self, material):
        for particle in self.particles:
            particle.material = material

    def traverse(self, o):
        if isinstance(o, (list, tuple)):
            for value in o:
                for subvalue in self.traverse(value):
                    yield subvalue
        else:
            yield o
