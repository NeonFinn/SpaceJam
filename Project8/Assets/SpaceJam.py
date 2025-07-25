from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.physics import PhysicsManager, ParticleSystemManager

import Classes as classesRef
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
            self.Universe = classesRef.Universe(self.loader, 'Universe/Universe.x', self.render, 'Universe',
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

            self.SpaceStation1 = classesRef.SpaceStation(self.loader, 'SpaceStation/spaceStation.x', self.render,'SpaceStation1',
                'SpaceStation/SpaceStation1_Dif2.png', (-2500, 1000, -100),30)

            self.fogZone = classesRef.FogZone(self.render, Vec3(2000, 2000, 200), 500)

            self.cTrav = CollisionTraverser()
            self.pusher = CollisionHandlerPusher()

            self.Player = Player.player(self.loader, self.taskMgr, self.accept, 'Spaceships/Dumbledore.x', self.render,
                                        'Player', 'Spaceships/spacejet_C.png', (0, 0, 0), 3.0, self)

            self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
            self.cTrav.addCollider(self.Player.collisionNode, self.pusher)

            for planet in [self.Planet1, self.Planet2, self.Planet3, self.Planet4, self.Planet5, self.Planet6]:
                self.pusher.addCollider(planet.collisionNode, planet.modelNode)
                self.cTrav.addCollider(planet.collisionNode, self.pusher)

            self.consumables = []

            # Powerups
            self.powerup1 = classesRef.Consumable(self.loader, self.render, 'Power1', Vec3(-500, 1500, 200), 25)
            self.powerup2 = classesRef.Consumable(self.loader, self.render, 'Power2', Vec3(1500, 800, -300), 25)
            self.powerup3 = classesRef.Consumable(self.loader, self.render, 'Power3', Vec3(-1200, -3000, 423), 25)
            self.powerup4 = classesRef.Consumable(self.loader, self.render, 'Power4', Vec3(-2000, -304, -260), 25)

            # add powerups to the list
            self.consumables.append(self.powerup1)
            self.consumables.append(self.powerup2)
            self.consumables.append(self.powerup3)
            self.consumables.append(self.powerup4)

            # add collision to powerups
            for powerup in self.consumables:
                self.pusher.addCollider(powerup.collisionNode, powerup.modelNode)
                self.cTrav.addCollider(powerup.collisionNode, self.pusher)

            self.Player.modelNode.setHpr(0, 0, 0)
            self.cloudDrones = []

            # MLB sentinel pattern
            self.Sentinel1 = classesRef.Orbiter(self.loader, self.taskMgr, "DroneDefender/DroneDefender.x", self.render,
                                             "Drone", 10.0, "DroneDefender/Drones.jpg", self.Planet5, 800, "MLB", self.Player)
            self.Sentinel2 = classesRef.Orbiter(self.loader, self.taskMgr, "DroneDefender/DroneDefender.x", self.render,
                                                "Drone", 10.0, "DroneDefender/Drones.jpg", self.Planet5, 800, "MLB", self.Player)

            # Cloud sentinel pattern
            self.Sentinel3 = classesRef.Orbiter(self.loader, self.taskMgr, "DroneDefender/DroneDefender.x", self.render,
                                             "Drone", 6.0, "DroneDefender/Drones.jpg", self.Planet2, 500, "Cloud", self.Player)
            self.Sentinel4 = classesRef.Orbiter(self.loader, self.taskMgr, "DroneDefender/DroneDefender.x", self.render,
                                                "Drone", 6.0, "DroneDefender/Drones.jpg", self.Planet2, 500, "Cloud", self.Player)

            # Wanderers
            self.Wanderer1 = classesRef.Wanderer(self.loader, "DroneDefender/DroneDefender.x", self.render, "Wanderer1",
                                                 "Drone", 6.0, "DroneDefender/Drones.jpg", self.Player, startPos=Vec3(0, 0, -100))
            self.Wanderer2 = classesRef.Wanderer(self.loader, "DroneDefender/DroneDefender.x", self.render, "Wanderer2",
                                                 "Drone", 6.0, "DroneDefender/Drones.jpg", self.Player, startPos=Vec3(100, -300, 100))

            self.pusher.addCollider(self.Wanderer1.collisionNode, self.Wanderer1.modelNode)
            self.cTrav.addCollider(self.Wanderer1.collisionNode, self.pusher)

            self.pusher.addCollider(self.Wanderer2.collisionNode, self.Wanderer2.modelNode)
            self.cTrav.addCollider(self.Wanderer2.collisionNode, self.pusher)

        SetupScene()
        self.enableHud()
        self.taskMgr.add(self.checkPowerupCollision, "CheckPowerupCollision")
        self.taskMgr.add(self.updateSystemsDownOverlay, 'UpdateSystemsDownOverlayTask')
        self.taskMgr.add(self.SpawnDrones, 'SpawnDronesTask')
        self.setCamera()

        self.boostTime = 0

        # Add systems down but hide until in fog zone
        self.systemsDownOverlay = OnscreenImage(image="Hud/warning.png", pos=(-.8, 0, 0.8), scale= 0.5)
        self.systemsDownOverlay.setTransparency(TransparencyAttrib.MAlpha)
        self.systemsDownOverlay.hide()

    def setCamera(self):
        self.disable_mouse()
        self.camera.reparentTo(self.Player.modelNode)
        self.camera.setFluidPos(0, 0, 0)

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()

        drone = classesRef.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                              droneName, 'DroneDefender/Drones.jpg', position, 5)
        self.cloudDrones.append(drone)
        drone.collisionNode.hide()

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud(radius=1)
        unitVec.normalize()
        position = unitVec * 700 + centralObject.modelNode.getPos()

        drone = classesRef.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                              droneName, 'DroneDefender/Drones.jpg', position, 5)
        self.cloudDrones.append(drone)
        drone.collisionNode.hide()

    def DrawCircleX(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleX(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300

            drone = classesRef.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                                  droneName, 'DroneDefender/Drones.jpg', position, 5)
            self.cloudDrones.append(drone)
            drone.collisionNode.hide()

    def DrawCircleY(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleY(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300

            drone = classesRef.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                                  droneName, 'DroneDefender/Drones.jpg', position, 5)
            self.cloudDrones.append(drone)
            drone.collisionNode.hide()


    def DrawCircleZ(self, droneName, radius = 1, numPoints = 100, step = 50):
        points = defensePaths.CircleZ(radius, numPoints)
        if step < len(points):
            unitVec = points[step]
            position = unitVec * 300

            drone = classesRef.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                                  droneName, 'DroneDefender/Drones.jpg', position, 5)
            self.cloudDrones.append(drone)
            drone.collisionNode.hide()

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
            classesRef.Drone.droneCount += 1
            droneName = f'Drone{classesRef.Drone.droneCount}'

            unitVec = defensePaths.Cloud(radius=1)
            unitVec.normalize()
            position = unitVec * 350 + self.Planet4.modelNode.getPos()

            drone = classesRef.Drone(self.loader, 'DroneDefender/DroneDefender.x', self.render,
                          droneName, 'DroneDefender/Drones.jpg', position, 5)

            self.cloudDrones.append(drone)
            drone.collisionNode.hide()
            self.pusher.addCollider(drone.collisionNode, drone.modelNode)
            self.cTrav.addCollider(drone.collisionNode, self.pusher)

        return task.cont

    def enableHud(self):
        self.Hud = OnscreenImage(image ="Hud/crosshair.png", pos = Vec3(0, 0, 0), scale = (0.05))
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)

    def updateSystemsDownOverlay(self, task):
        playerPos = self.Player.modelNode.getPos()
        if self.fogZone.inside(playerPos):
            self.systemsDownOverlay.show()
        else:
            self.systemsDownOverlay.hide()
        return task.cont

    def checkPowerupCollision(self, task):
        playerPos = self.Player.modelNode.getPos()
        for powerup in self.consumables:
            if not powerup.collected:
                dist = (powerup.modelNode.getPos() - playerPos).length()
                if dist < 50:
                    powerup.collect()
                    self.activateBoost()
        return task.cont

    def activateBoost(self):
        self.Player.speedMultiplier = 2.0
        self.Player.fireRateBoost = True
        self.Player.fireCooldown = 0.2  # ↓ reduce fire delay
        self.boostTime = 5.0
        self.taskMgr.add(self.handleBoostTimer, "BoostTimerTask")

    def handleBoostTimer(self, task):
        dt = globalClock.getDt()
        self.boostTime -= dt
        if self.boostTime <= 0:
            self.Player.speedMultiplier = 1.0
            self.Player.fireRateBoost = False
            self.Player.fireCooldown = self.Player.originalFireCooldown  # reset properly
            return task.done
        return task.cont

app = MyApp() # create instance of MyApp
app.run() # run application