import pygame as game


class App:

    running = True  # keep the application running
    screen = None  # window handler pointer
    title = "Application"  # application window title
    size = (0, 0)  # application window size
    center = (0, 0)  # application window position
    flags = game.HWSURFACE | game.DOUBLEBUF  # hardware acceleration and double buffering
    framerate = 30  # application frame rate
    t = 0  # время с начала симуляции

    def __init__(self, t="Application", x=550, y=400, f=30):
        self.title = t
        self.size = (x, y)
        self.center = (x / 2, y / 2)
        self.framerate = f
        self.Initialize()

    def Run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen = game.display.set_mode(self.size, self.flags)
        self.running = True

        while self.running:
            for event in game.event.get():
                self.HandleEvent(event)
            self.t += 1 / 30
            self.Update()
            self.Render()
            game.time.delay(int(1000 / self.framerate))
        self.CleanUp()

    def HandleEvent(self, event):
        if event.type == game.QUIT:
            self.running = False

    def CleanUp(self):
        game.quit()

    def Exit(self):
        self.running = False

    def Initialize(self):
        pass

    def Update(self):
        pass

    def Render(self):
        pass
