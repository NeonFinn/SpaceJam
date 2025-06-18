from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        def SetupScene():
            self.universe = self.loader.loadModel('Universe/Universe.x')
            self.universe.reparentTo(self.render)
            self.universe.setScale(15000)
            tex = self.loader.loadTexture('Universe/starfield-in-blue.jpg')
            self.universe.setTexture(tex, 1)

            self.Planet1 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet1.reparentTo(self.render)
            self.Planet1.setPos(1800, 3000, -1500)  # randomize planet position later
            self.Planet1.setScale(350)
            tex = self.loader.loadTexture('Planets/Jupiter.jpg')
            self.Planet1.setTexture(tex, 1)

            self.Planet2 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet2.reparentTo(self.render)
            self.Planet2.setPos(-1900, 4950, 1700)  # randomize planet position later
            self.Planet2.setScale(350)
            tex = self.loader.loadTexture('Planets/Mars.jpg')
            self.Planet2.setTexture(tex, 1)

            self.Planet3 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet3.reparentTo(self.render)
            self.Planet3.setPos(900, 5300, 2000)
            self.Planet3.setScale(350)
            tex = self.loader.loadTexture('Planets/Mercury.jpg')
            self.Planet3.setTexture(tex, 1)

            self.Planet4 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet4.reparentTo(self.render)
            self.Planet4.setPos(-1200, 5000, -1800)
            self.Planet4.setScale(350)
            tex = self.loader.loadTexture('Planets/Neptune.jpg')
            self.Planet4.setTexture(tex, 1)

            self.Planet5 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet5.reparentTo(self.render)
            self.Planet5.setPos(0, 4850, 0)
            self.Planet5.setScale(350)
            tex = self.loader.loadTexture('Planets/Uranus.jpg')
            self.Planet5.setTexture(tex, 1)

            self.Planet6 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet6.reparentTo(self.render)
            self.Planet6.setPos(1600, 5200, 800)
            self.Planet6.setScale(350)
            tex = self.loader.loadTexture('Planets/Venus.jpg')
            self.Planet6.setTexture(tex, 1)

            self.SpaceStation = self.loader.loadModel('SpaceStation/spaceStation.x')
            self.SpaceStation.reparentTo(self.render)
            self.SpaceStation.setPos(-10000, 3000, 3000)
            self.SpaceStation.setScale(500)
            tex = self.loader.loadTexture('SpaceStation/SpaceStation1_Dif2.png')
            self.SpaceStation.setTexture(tex, 1)

            self.Player = self.loader.loadModel('Spaceships/Dumbledore.x')
            self.Player.reparentTo(self.render)
            self.Player.setPos(0, 0, 0)
            self.Player.setScale(1)
            tex = self.loader.loadTexture('Spaceships/spacejet_C.png')
            self.Player.setTexture(tex, 1)

        SetupScene()

app = MyApp() # create instance of MyApp
app.run() # run application