from cmath import cos, sin
import pygame as game
from App import *
from VerletPhysics import *

count = 50
initial_length = 30  # Здесь задается длина пружины
global stiffness_value  # Здесь задается жесткость пружины
stiffness_value = 1

class DemoRope(App):
    world = World(Vector(10000.0, 10000.0), Vector(0, 1), 4)
    grabbed = None
    radius = 20
    strength = 0.20
    scale = 1.0
    offset = Vector(0, 0)
    oscillation_mode = None  # 'x' for horizontal, 'y' for vertical
    oscillating_particle = None
    oscillating_particle_1 = None
    oscillating_particle_2 = None
    oscillation_amplitude_x = 200  # Small amplitude for x-axis
    oscillation_amplitude_y = 2  # Smaller amplitude for y-axis
    oscillation_frequency_x = 10  # Frequency of oscillation
    oscillation_frequency_y = 10
    spatial_time = 0.1  # Задержка между колебаниями
    time_since_last_oscillation_x = 0
    time_since_last_oscillation_y = 0
    mass_changed = False
    positioned = False  # Flag to fix the position after initial adjustment

    

    def Initialize(self):
        rope = self.world.AddComposite()
        particles = list()
        j = 0
        self.recording = False

        for i in range(0, count):
            particle = self.world.AddParticle(self.world.hsize.x, 10.0 + j)
            particle.velocity = Vector(0, 0)
            particles.append(particle)
            j += 55
        rope.AddParticles(*particles)

        # Fix the top particle, set up the bottom as oscillating
        rope.particles[0].material.mass = 0.0
        rope.particles[-1].material.mass = 0.0
        self.oscillating_particle = rope.particles[-1]
        self.oscillating_particle_1 = rope.particles[0]
        # self.oscillating_particle_2 = rope.particles[-25]


        # Gradually adjust bottom particle to position all particles just above it
        for i, particle in enumerate(particles[1:], start=1):
            initial_length = (particles[1].position.y - particles[0].position.y) * 1
            particle.position.y = particles[0].position.y + initial_length * i

        # Add constraints with reduced stiffness
        constraints = list()
        for i in range(0, count - 1):
            constraint = self.world.AddConstraint(
                rope.particles[i], rope.particles[i + 1], stiffness_value, initial_length
            )
            constraints.append(constraint)
        rope.AddConstraints(*constraints)

    def Update(self):
        keys = game.key.get_pressed()
        time_elapsed = self.t  # Corrected simulation time

        if keys[game.K_EQUALS] or keys[game.K_KP_PLUS]:
            self.scale *= 1.1
            self.AdjustOffset()
        if keys[game.K_MINUS] or keys[game.K_KP_MINUS]:
            self.scale /= 1.1
            self.AdjustOffset()

        if keys[game.K_y]:
            self.StartGraphRecording()  # Начать запись смещений
        if keys[game.K_f]:
            self.StopGraphRecording()

        if self.recording:
            dt = self.t
            # for i in self.y_displacements.keys():
            #     particle = self.world.particles[i]
            #     displacement = particle.position.y - self.initial_y_positions[i]
            #     self.y_displacements[i].append(displacement)
            #     # Скорость продольной волны по изменению смещения
            #     speed = (displacement - self.prev_y_displacements[i]) / dt
            #     self.y_speeds[i].append(speed)
            #     # Обновляем предыдущее смещение
            #     self.prev_y_displacements[i] = displacement
            for i in self.x_displacements.keys():
                particle = self.world.particles[i]
                displacement = particle.position.x - self.initial_x_positions[i]
                self.x_displacements[i].append(displacement)
                # Скорость продольной волны по изменению смещения
                speed = (displacement - self.prev_x_displacements[i]) / dt
                self.x_speeds[i].append(speed)
                # Обновляем предыдущее смещение
                self.prev_x_displacements[i] = displacement
        
        if keys[game.K_s]:
            self.oscillating_particle = max(
                self.world.particles[1:],  # Exclude the fixed top particle
                key=lambda p: (p.position - self.world.particles[0].position).magnitude()
            )
            self.oscillating_particle.material.mass = 0.0  # Закрепляем грузик
            self.oscillating_particle_1.material.mass = 0.0
            self.is_fixed = True

        if keys[game.K_x]:
            self.oscillation_mode = 'x'
            self.StartGraphRecording()  # Start recording y-displacements
        elif keys[game.K_y]:
            self.oscillation_mode = 'y'
            # self.StartGraphRecording()  # Start recording y-displacements
        elif keys[game.K_1] and self.oscillation_mode == 'x':
            self.oscillation_mode = None  # Stop horizontal oscillation
        elif keys[game.K_2] and self.oscillation_mode == 'y':
            self.oscillation_mode = None  # Stop vertical oscillation

        # center_x = (self.world.particles[0].position.x + self.oscillating_particle.position.x) / 2
        center_x = self.world.hsize.x
        # center_x_1 = (self.world.particles[0].position.x + self.oscillating_particle_1.position.x) / 2
        center_x_1 = self.world.hsize.x
        # center_x_2 = (self.world.particles[0].position.x + self.oscillating_particle_2.position.x) / 2
        if self.oscillation_mode == 'x':
            self.time_since_last_oscillation_x += time_elapsed
            if self.time_since_last_oscillation_x >= self.spatial_time:
                new_x = center_x + self.oscillation_amplitude_x * sin(self.oscillation_frequency_x * time_elapsed).real
                new_x_1 = center_x_1 + self.oscillation_amplitude_x * (-1) * sin(self.oscillation_frequency_x * time_elapsed).real
                # new_x_1 = center_x_1 + self.oscillation_amplitude_x * sin(self.oscillation_frequency_x * time_elapsed).real
                # new_x_2 = center_x_2 + self.oscillation_amplitude_x *(-1)* sin(self.oscillation_frequency_x * time_elapsed).real
                self.oscillating_particle.position.x = new_x
                self.oscillating_particle_1.position.x = new_x_1
                # self.oscillating_particle_2.position.x = new_x_2
                self.time_since_last_oscillation_x = 0
            

        elif self.oscillation_mode == 'y':
            self.time_since_last_oscillation_y += time_elapsed
            if self.time_since_last_oscillation_y >= self.spatial_time:
                new_y = self.oscillating_particle.position.y + \
                         self.oscillation_amplitude_y * sin(self.oscillation_frequency_y * time_elapsed).real
                self.oscillating_particle.position.y = min(max(new_y, 0), self.world.hsize.y)
                self.time_since_last_oscillation_y = 0  # Сброс таймера после колебания

        if keys[game.K_m] and not self.mass_changed:
            mid_particle = self.world.particles[len(self.world.particles) // 2]
            mid_particle.material.mass *= 2
            mid_particle.color = (255, 0, 0)  # Change to red
            self.mass_changed = True

        if keys[game.K_UP]:
            self.offset.y += 10
        if keys[game.K_DOWN]:
            self.offset.y -= 10
        if keys[game.K_LEFT]:
            self.offset.x += 10
        if keys[game.K_RIGHT]:
            self.offset.x -= 10

        if not self.positioned:
            self.oscillating_particle.position.y = max(
                p.position.y for p in self.world.particles[:-1]) + 1
            self.oscillating_particle.material.mass = 0.0
            self.positioned = True

        if game.mouse.get_pressed()[0]:
            if self.grabbed is None:
                closest = self.ClosestPoint()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed is not None:
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
                int(c.node1.position.x * self.scale + self.offset.x),
                int(c.node1.position.y * self.scale + self.offset.y))
            pos2 = (
                int(c.node2.position.x * self.scale + self.offset.x),
                int(c.node2.position.y * self.scale + self.offset.y))
            game.draw.line(self.screen, (0, 255, 0), pos1, pos2, 3)
        for p in self.world.particles:
            pos = (int(p.position.x * self.scale + self.offset.x), int(p.position.y * self.scale + self.offset.y))
            color = (255, 0, 0) if hasattr(p, 'color') and p.color == (255, 0, 0) else (255, 255, 255)
            game.draw.circle(self.screen, color, pos, int(5 * self.scale), 0)
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


    def StartGraphRecording(self):
        # Инициализировать начальные позиции для отслеживания смещений
        # self.y_displacements = {i: [] for i in range(0, len(self.world.particles)-11, 1)}
        # self.initial_y_positions = {i: self.world.particles[i].position.y for i in self.y_displacements.keys()}
        # self.prev_y_displacements = {i: self.initial_y_positions[i] for i in self.y_displacements.keys()}
        # self.y_speeds = {i: [] for i in self.y_displacements.keys()}  # Словарь для записи скоростей

        self.x_displacements = {i: [] for i in range(0, len(self.world.particles)-11, 1)}
        self.initial_x_positions = {i: self.world.particles[i].position.x for i in self.x_displacements.keys()}
        self.prev_x_displacements = {i: self.initial_x_positions[i] for i in self.x_displacements.keys()}
        self.x_speeds = {i: [] for i in self.x_displacements.keys()}  # Словарь для записи скоростей
        self.recording = True  # Включаем флаг записи

    def StopGraphRecording(self):
        import matplotlib.pyplot as plt
        # Завершить запись и построить график
        self.recording = False  # Отключаем флаг записи

        # Построение графиков смещения и скорости
        fig, axs = plt.subplots(2, 1, figsize=(10, 8))

        # График смещения
        for i, displacements in self.x_displacements.items():
            if i > 23 and i < 27:
                axs[0].plot([abs(x) for x in displacements], label=f"Particle {i}")
        axs[0].set_xlabel("Time")
        axs[0].set_ylabel("X Displacement from Initial Position")
        axs[0].legend()
        axs[0].set_title("X Displacement Over Time")
        """
        # График скорости
        for i, speeds in self.y_speeds.items():
            axs[1].plot(speeds, label=f"Particle {i}")
        axs[1].set_xlabel("Time")
        axs[1].set_ylabel("Speed of Longitudinal Wave")
        axs[1].legend()
        axs[1].set_title("Speed of Longitudinal Wave Over Time")
        """
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = DemoRope("Application", 1000, 900, 60)
    app.Run()