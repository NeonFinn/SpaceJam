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
            self.Player = Classes.Player(self.loader, 'Spaceships/Dumbledore.x', self.render, 'Player', 'Spaceships/spacejet_C.png', Vec3(0, 0, 0), 3)
            self.Player.modelNode.setHpr(0, 90, 0)
            self.cloudDrones = []

        SetupScene()
        self.taskMgr.add(self.SpawnDrones, 'SpawnDrones')

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        maxCloudDrones = 300

        if len(self.cloudDrones) < maxCloudDrones and Classes.Drone.droneCount % 4 == 0:
            unitVec = defensePaths.Cloud(radius=1)
            unitVec.normalize()
            position = unitVec * 700 + centralObject.modelNode.getPos()

            newDrone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 10)
            self.cloudDrones.append(newDrone)

    def DrawCircleX(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleX(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300
            newDrone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 8)
            newDrone.modelNode.setColor(1, 0, 0, 1)

    def DrawCircleY(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleY(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300
            newDrone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 8)
            newDrone.modelNode.setColor(0, 1, 0, 1)

    def DrawCircleZ(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleZ(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300
            newDrone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render, droneName, 'DroneDefender/Drones.jpg', position, 8)
            newDrone.modelNode.setColor(0, 0, 1, 1)

    def SpawnDrones(self, task):
        fullCycle = 60
        step = task.frame % fullCycle

        Classes.Drone.droneCount += 1
        droneName = f'Drone{Classes.Drone.droneCount}'

        self.DrawCloudDefense(self.Planet4, droneName)
        self.DrawBaseballSeams(self.SpaceStation1, droneName, step, numSeams = 60)
        self.DrawCircleX(droneName = droneName, radius = 3, numPoints = 60, step = step)
        self.DrawCircleY(droneName = droneName, radius = 3, numPoints = 60, step = step)
        self.DrawCircleZ(droneName = droneName, radius = 3, numPoints = 60, step = step)

        return task.cont

app = MyApp() # create instance of MyApp
app.run() # run application