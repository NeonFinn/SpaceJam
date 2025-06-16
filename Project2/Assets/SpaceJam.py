from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

import Classes as Classes
import DefensePaths as defensePaths

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        def SetupScene():
            self.Universe = Classes.Universe(self.loader, 'Universe/Universe.x', self.render, 'Universe', 'Universe/starfield-in-blue.jpg', (0, 0, 0), 10000)

            self.Planet1 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet1', 'Planets/Jupiter.jpg', (-6000, -3000, -800), 250)
            self.Planet2 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet2', 'Planets/Mars.jpg', (800, 6000, 0), 300)
            self.Planet3 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet3', 'Planets/Mercury.jpg', (500, -5000, 1000), 500)
            self.Planet4 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet4', 'Planets/Neptune.jpg', (-1200, 6000, 500), 150)
            self.Planet5 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet5', 'Planets/Uranus.jpg', (-2000, -2000, 3000), 500)
            self.Planet6 = Classes.Planet(self.loader, 'Planets/protoPlanet.x', self.render, 'Planet6', 'Planets/Venus.jpg', (3000, -900, -1400), 700)

            self.SpaceStation1 = Classes.SpaceStation(self.loader, 'SpaceStation/spaceStation.x', self.render, 'SpaceStation1', 'SpaceStation/SpaceStation1_Dif2.png', (-2500, 1000, -100), 40)
            self.Hero = Classes.Player(self.loader, 'DroneDefender/DroneDefender.x', self.render, 'Player', 'DroneDefender/Drones.jpg', Vec3(0, 0, 0), 50)

        SetupScene()
        self.taskMgr.add(self.SpawnDrones, 'SpawnDrones')  # add task to spawn drones

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud(radius = 1)
        unitVec.normalize()
        position = unitVec * 700 + centralObject.modelNode.getPos()
        if Classes.Drone.droneCount % 4 == 0:
            Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 10)

    def DrawCircleX(self, centralObject, droneName, radius = 1, numPoints = 100, step = 0):
        points = defensePaths.CircleX(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300
            Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 10)

    def DrawCircleY(self, centralObject, droneName, radius = 1, numPoints = 100, step = 0):
        points = defensePaths.CircleY(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300
            Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 10)

    def DrawCircleZ(self, centralObject, droneName, radius = 1, numPoints = 100, step = 0):
        points = defensePaths.CircleZ(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300
            Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 10)

    def SpawnDrones(self, task):
        fullCycle = 60
        step = task.frame % fullCycle

        Classes.Drone.droneCount += 1
        droneName = f'Drone{Classes.Drone.droneCount}'

        self.DrawCloudDefense(self.Planet4, droneName)
        self.DrawBaseballSeams(self.SpaceStation1, droneName, step, numSeams = 60)
        self.DrawCircleX(None, droneName, radius = 3, numPoints = 60, step = step)
        self.DrawCircleY(None, droneName, radius = 3, numPoints = 60, step = step)
        self.DrawCircleZ(None, droneName, radius = 3, numPoints = 60, step = step)

        return task.cont

app = MyApp() # create instance of MyApp
app.run() # run application