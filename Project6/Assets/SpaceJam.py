from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.physics import PhysicsManager, ParticleSystemManager

import Classes
import DefensePaths as defensePaths
import CollideObjectBase
import Player

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Initialize physics manager
        self.physicsMgr = PhysicsManager()
        base.physicsMgr = self.physicsMgr

        # Initialize particle manager
        self.particleMgr = ParticleSystemManager()
        base.particleMgr = self.particleMgr

        self.enableParticles() # Call function to actually let particles show up... I forgot last time

        def SetupScene():
            self.Universe = Classes.Universe(self.loader, 'Universe/Universe.x', self.render, 'Universe',
                                             'Universe/starfield-in-blue.jpg', Vec3(0, 0, 0), 10000)

            self.Planet1 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,'Planet1',
                'Planets/Jupiter.jpg', (-6000, -3000, -800), 250, colRadius= 1.1)
            self.Planet2 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,'Planet2',
                'Planets/Mars.jpg', (800, 6000, -700), 300, colRadius= 1.1)
            self.Planet3 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,'Planet3',
                'Planets/Mercury.jpg', (1000, -8000, 1000), 500, colRadius= 1.1)
            self.Planet4 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,'Planet4',
                'Planets/Neptune.jpg', (-1200, 6000, 500), 150, colRadius= 1.1)
            self.Planet5 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,'Planet5',
                'Planets/Uranus.jpg', (-5000, 8000, -2000), 500, colRadius= 1.1)
            self.Planet6 = CollideObjectBase.SphereCollideObject(self.loader, 'Planets/protoPlanet.x', self.render,'Planet6',
                'Planets/Venus.jpg', (4000, -2300, -1400), 300, colRadius= 1.1)

            self.SpaceStation1 = Classes.SpaceStation(self.loader, 'SpaceStation/spaceStation.x', self.render,'SpaceStation1',
                'SpaceStation/SpaceStation1_Dif2.png', (-2500, 1000, -100),30)

            self.fogZone = Classes.FogZone(self.render, Vec3(2000, 2000, 200), 500)

            self.cTrav = CollisionTraverser()
            self.pusher = CollisionHandlerPusher()

            self.Player = Player.player(self.loader, self.taskMgr, self.accept, 'Spaceships/Dumbledore.x', self.render,
                                        'Player', 'Spaceships/spacejet_C.png', (0, 0, 0), 3.0, self)

            self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
            self.cTrav.addCollider(self.Player.collisionNode, self.pusher)

            for planet in [self.Planet1, self.Planet2, self.Planet3, self.Planet4, self.Planet5, self.Planet6]:
                self.pusher.addCollider(planet.collisionNode, planet.modelNode)
                self.cTrav.addCollider(planet.collisionNode, self.pusher)

            self.Player.modelNode.setHpr(0, 0, 0)
            self.cloudDrones = []

        SetupScene()
        self.enableHud()
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

        drone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                              droneName, 'DroneDefender/Drones.jpg', position, 5)
        self.cloudDrones.append(drone)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud(radius=1)
        unitVec.normalize()
        position = unitVec * 700 + centralObject.modelNode.getPos()

        drone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                              droneName, 'DroneDefender/Drones.jpg', position, 5)
        self.cloudDrones.append(drone)

    def DrawCircleX(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleX(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300

            drone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                                  droneName, 'DroneDefender/Drones.jpg', position, 5)
            self.cloudDrones.append(drone)

    def DrawCircleY(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleY(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300

            drone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                                  droneName, 'DroneDefender/Drones.jpg', position, 5)
            self.cloudDrones.append(drone)


    def DrawCircleZ(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleZ(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300

            drone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                                  droneName, 'DroneDefender/Drones.jpg', position, 5)
            self.cloudDrones.append(drone)

    def SpawnDrones(self, task):
        if task.frame == 0:
            for i in range(60):
                self.DrawCircleX(droneName=f'DroneX_{i}', radius=3, numPoints=60, step=i)
                self.cloudDrones[-1].modelNode.setColor(1, 0, 0, 1)

                self.DrawCircleY(droneName=f'DroneY_{i}', radius=3, numPoints=60, step=i)
                self.cloudDrones[-1].modelNode.setColor(0, 1, 0, 1)

                self.DrawCircleZ(droneName=f'DroneZ_{i}', radius=3, numPoints=60, step=i)
                self.cloudDrones[-1].modelNode.setColor(0, 0, 1, 1)

            for i in range(60):
                droneName = f'BaseballSeam_{i}'
                self.DrawBaseballSeams(self.SpaceStation1, droneName, i, numSeams=60)

        maxCloudDrones = 400
        if len(self.cloudDrones) >= maxCloudDrones:
            return task.cont

        while len(self.cloudDrones) < maxCloudDrones:
            Classes.Drone.droneCount += 1
            droneName = f'Drone{Classes.Drone.droneCount}'

            unitVec = defensePaths.Cloud(radius=1)
            unitVec.normalize()
            position = unitVec * 350 + self.Planet4.modelNode.getPos()

            drone = Classes.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                          droneName, 'DroneDefender/Drones.jpg', position, 5)

            self.cloudDrones.append(drone)
            self.pusher.addCollider(drone.collisionNode, drone.modelNode)
            self.cTrav.addCollider(drone.collisionNode, self.pusher)

        return task.cont

    def enableHud(self):
        self.Hud = OnscreenImage(image ="Hud/crosshair.png", pos = Vec3(0, 0, 0), scale = (0.05))
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)

app = MyApp() # create instance of MyApp
app.run() # run application