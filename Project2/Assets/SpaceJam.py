from direct.showbase.ShowBase import ShowBase
import Classes as Classes
import DefensePaths as defensePaths

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        def SetupScene():

            self.Universe = Classes.Universe(self.loader, 'Universe/Universe.x', self.render, 'Universe', 'Universe/starfield-in-blue.jpg', (0, 0, 0), 10000)

            self.Planet1 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet1', 'Planets/planet-texture.jpg', (-6000, -3000, -800), 250)
            self.Planet2 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet2', 'Planets/planet-texture.jpg', (0, 6000, 0), 300)
            self.Planet3 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet3', 'Planets/planet-texture.jpg', (500, -5000, 200), 500)
            self.Planet4 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet4', 'Planets/planet-texture.jpg', (300, 6000, 500), 150)
            self.Planet5 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet5', 'Planets/planet-texture.jpg', (700, -2000, 100), 500)
            self.Planet6 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet6', 'Planets/planet-texture.jpg', (0, -900, -1400), 700)

            self.SpaceStation1 = Classes.SpaceStation(self.loader, 'SpaceStation/spaceStation.x', self.render, 'SpaceStation1', 'SpaceStation/space-station-texture.jpg', (1500, 1000, -100), 40)
            self.Hero = Classes.SpaceShip(self.loader, 'Spaceship/heroShip.x', self.render, 'Hero', 'Spaceship/hero-ship-texture.jpg', Vec3(1000, 1200, -50), 50)

        def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
            unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
            unitVec.normalize()
            position = unitVec * radius * 250 + centralObject.modelNode.getPos()
            Classes.Drone(self.loader, 'DroneDefender/DroneDefender.obj', self.render, droneName, 'Drone/drone-texture.jpg', position, 5)

        def DrawCloudDefense(self, centralObject, droneName):
            unitVec = defensePaths.Cloud(radius = 1)
            unitVec.normalize()
            position = unitVec * 500 + centralObject.modelNode.getPos()
            Classes.Drone(self.loader, 'DroneDefender/DroneDefender.obj', self.render, droneName, 'Drone/drone-texture.jpg', position, 10)

        SetupScene()

        fullCycle = 60

        for j in range(fullCycle):
            Classes.Drone.droneCount +=1
            droneName = "Drone" + str(Classes.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, droneName)
            self.DrawBaseballSeams(self.SpaceStation1, droneName, j, fullCycle, 2)


app = MyApp() # create instance of MyApp
app.run() # run application