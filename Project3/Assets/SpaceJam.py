from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *

import Classes as Classes
import DefensePaths as defensePaths

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.keyMap = {
            "forward": False,
            "turnLeft": False,
            "turnRight": False,
            "turnUp": False,
            "turnDown": False,
            "rollLeft": False,
            "rollRight": False,
        }

        self.accept("space", self.setKey, ["forward", True])
        self.accept("space-up", self.setKey, ["forward", False])
        self.accept("a", self.setKey, ["turnLeft", True])
        self.accept("a-up", self.setKey, ["turnLeft", False])
        self.accept("d", self.setKey, ["turnRight", True])
        self.accept("d-up", self.setKey, ["turnRight", False])
        self.accept("w", self.setKey, ["turnUp", True])
        self.accept("w-up", self.setKey, ["turnUp", False])
        self.accept("s", self.setKey, ["turnDown", True])
        self.accept("s-up", self.setKey, ["turnDown", False])
        self.accept("q", self.setKey, ["rollLeft", True])
        self.accept("q-up", self.setKey, ["rollLeft", False])
        self.accept("e", self.setKey, ["rollRight", True])
        self.accept("e-up", self.setKey, ["rollRight", False])

        self.taskMgr.add(self.updatePlayer, 'updatePlayerTask')
        self.taskMgr.add(self.SpawnDrones, 'SpawnDrones')

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
        self.cameraFollow()
        self.taskMgr.add(self.updateCamera, 'updateCameraTask')

    def setKey(self, key, value):
        self.keyMap[key] = value

    def updatePlayer(self, task):
        playerNode = self.Player.modelNode
        speed = 1
        rotationSpeed = 60 * globalClock.getDt()

        if self.keyMap["forward"]:
            playerNode.setPos(playerNode, 0, speed, 0)

        if self.keyMap["turnLeft"]:
            playerNode.setH(playerNode, rotationSpeed)

        if self.keyMap["turnRight"]:
            playerNode.setH(playerNode, -rotationSpeed)

        if self.keyMap["turnUp"]:
            playerNode.setP(playerNode, rotationSpeed)

        if self.keyMap["turnDown"]:
            playerNode.setP(playerNode, -rotationSpeed)

        if self.keyMap["rollLeft"]:
            playerNode.setR(playerNode, rotationSpeed)

        if self.keyMap["rollRight"]:
            playerNode.setR(playerNode, -rotationSpeed)

        return task.cont

    def cameraFollow(self):
        self.camera.reparentTo(self.Player.modelNode)
        self.camera.setH(self.Player.modelNode.getH())

    def updateCamera(self, task):
        self.camera.setH(self.Player.modelNode.getH())
        self.camera.setP(0)
        self.camera.setR(0)
        self.camera.lookAt(self.Player.modelNode)
        return task.cont

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