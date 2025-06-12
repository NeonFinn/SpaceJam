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
            self.Planet1.setPos(1800, 1500, -1500)  # randomize planet position later
            self.Planet1.setScale(350)

            self.Planet2 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet2.reparentTo(self.render)
            self.Planet2.setPos(-1900, 4950, 1700)  # randomize planet position later
            self.Planet2.setScale(350)

            self.Planet3 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet3.reparentTo(self.render)
            self.Planet3.setPos(900, 5300, 2000)  # randomize planet position later
            self.Planet3.setScale(350)

            self.Planet4 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet4.reparentTo(self.render)
            self.Planet4.setPos(-1200, 5000, -1800)  # randomize planet position later
            self.Planet4.setScale(350)

            self.Planet5 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet5.reparentTo(self.render)
            self.Planet5.setPos(0, 4850, 0)  # randomize planet position later
            self.Planet5.setScale(350)

            self.Planet6 = self.loader.loadModel('Planets/protoPlanet.x')
            self.Planet6.reparentTo(self.render)
            self.Planet6.setPos(1600, 5200, 800)  # randomize planet position later
            self.Planet6.setScale(350)

        SetupScene()

app = MyApp() # create instance of MyApp
app.run() # run application