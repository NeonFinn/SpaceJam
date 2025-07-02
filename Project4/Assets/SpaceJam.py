from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher

import Classes as Classes
import DefensePaths as defensePaths
import CollideObjectBase
import Player as Player

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        def SetupScene():
            self.Universe = Classes.Universe(self.loader, 'Universe/Universe.x', self.render, 'Universe',
                                             'Universe/starfield-in-blue.jpg', Vec3(0, 0, 0), 10000)

            self.Planet1 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,
                                                                 'Planet1',
                                                                 'Planets/Jupiter.jpg', (-6000, -3000, -800), 250)
            self.Planet2 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,
                                                                 'Planet2',
                                                                 'Planets/Mars.jpg', (800, 6000, 0), 300)
            self.Planet3 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,
                                                                 'Planet3',
                                                                 'Planets/Mercury.jpg', (5500, -5000, 1000), 500)
            self.Planet4 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,
                                                                 'Planet4',
                                                                 'Planets/Neptune.jpg', (-1200, 6000, 500), 150)
            self.Planet5 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,
                                                                 'Planet5',
                                                                 'Planets/Uranus.jpg', (-5000, 3000, -4000), 500)
            self.Planet6 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,
                                                                 'Planet6',
                                                                 'Planets/Venus.jpg', (4000, -1300, -1400), 300)

            self.SpaceStation1 = Classes.SpaceStation(self.loader, 'SpaceStation/spaceStation.x', self.render,
                                                      'SpaceStation1',
                                                      'SpaceStation/SpaceStation1_Dif2.png', (-2500, 1000, -100),
                                                      30)

            self.Player = Player.player(self.loader, self.taskMgr, self.accept, 'Spaceships/Dumbledore.x', self.render,
                                        'Player', 'Spaceships/spacejet_C.png', (0, 0, 0), 3.0, self)

            self.cTrav = CollisionTraverser()
            self.pusher = CollisionHandlerPusher()

            self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
            self.cTrav.addCollider(self.Player.collisionNode, self.pusher)

            for planet in [self.Planet1, self.Planet2, self.Planet3, self.Planet4, self.Planet5, self.Planet6]:
                self.pusher.addCollider(planet.collisionNode, planet.modelNode)
                self.cTrav.addCollider(planet.collisionNode, self.pusher)

            self.cTrav.addCollider(self.Universe.collisionNode, self.pusher)

            self.cTrav.showCollisions(self.render)

            self.Player.modelNode.setHpr(0, 0, 0)
            self.cloudDrones = []

        SetupScene()
        self.taskMgr.add(self.SpawnDrones, 'SpawnDronesTask')
        self.setCamera()

    def setCamera(self):
        self.disable_mouse()
        self.camera.reparentTo(self.Player.modelNode)
        self.camera.setFluidPos(0, 0, 0)

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

        if task.frame == 0:
            for i in range(60):
                name = f'DroneX_{i}'
                self.DrawCircleX(droneName=name, radius=3, numPoints=60, step=i)

                name = f'DroneY_{i}'
                self.DrawCircleY(droneName=name, radius=3, numPoints=60, step=i)

                name = f'DroneZ_{i}'
                self.DrawCircleZ(droneName=name, radius=3, numPoints=60, step=i)

        if task.frame % 2 == 0:
            Classes.Drone.droneCount += 1
            droneName = f'Drone{Classes.Drone.droneCount}'
            self.DrawBaseballSeams(self.SpaceStation1, droneName, step, numSeams=60)
        elif task.frame % 5 == 0:
            Classes.Drone.droneCount += 1
            droneName = f'Drone{Classes.Drone.droneCount}'
            self.DrawCloudDefense(self.Planet4, droneName)

        return task.cont

app = MyApp() # create instance of MyApp
app.run() # run application