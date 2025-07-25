from direct.interval.IntervalGlobal import Sequence

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, Vec3, TransparencyAttrib
from CollideObjectBase import *
from direct.task.Task import TaskManager
import DefensePaths as defensePaths

class Planet(ShowBase):
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.node().addSolid(CollisionSphere(0,0,0, 1.25))
        self.collisionNode.show()

class Drone(ShowBase):
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.node().addSolid(CollisionSphere(0, 0, 0, 5))
        self.collisionNode.show()

        Drone.droneCount += 1

class SpaceStation(CapsuleCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
                 texPath: str, posVec, scaleVec):
        super().__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Missile(SphereCollideObject):
    missileBay = 1
    missileDistance = 4000
    reloadTime = 0.25

    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    intervals = {}

    missileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), scaleVec, 3.0)

        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.node().addSolid(CollisionSphere(0, 0, 0, 3.0))

        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)

# Create spherical fog zone
class FogZone:
    def __init__(self, render, position: Vec3, radius: float):
        self.node = render.attachNewNode("FogZone")
        self.node.setPos(position)

        self.fogVisual = loader.loadModel("models/misc/sphere")
        self.fogVisual.reparentTo(self.node)
        self.fogVisual.setScale(radius)
        self.fogVisual.setColor(0.5, 0.5, 0.5, 0.1)
        self.fogVisual.setTransparency(TransparencyAttrib.MAlpha)
        self.fogVisual.setTwoSided(True)

    # Check radius
    def inside(self, point: Vec3) -> bool:
        return (point - self.node.getPos()).length() < self.fogVisual.getScale().getX()

class Orbiter(SphereCollideObject):
    numOrbits = 0
    velocity = 0.05
    cloudTimer = 240
    def __init__(self, loader: Loader, taskMgr: TaskManager, modelPath: str, parentNode: NodePath, nodeName: str, scaleVec: Vec3, texPath: str,
                 centralObject: PlacedObject, orbitRadius: float, orbitType: str, staringAt: Vec3):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2, 3.2)

        self.taskMgr = taskMgr
        self.orbitType = orbitType
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.orbitObject = centralObject
        self.orbitRadius = orbitRadius
        self.staringAt = staringAt

        Orbiter.numOrbits += 1
        self.orbitIndex = Orbiter.numOrbits

        self.cloudClock = 0

        self.taskFlag = "Traveler-" + str(self.orbitIndex)
        self.taskMgr.add(self.Orbit, self.taskFlag)

    def Orbit(self, task):
        if self.orbitType == "MLB":
            positionVec = defensePaths.BaseballSeams(task.time * Orbiter.velocity, self.orbitIndex, 2.0)
            self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())
            self.modelNode.lookAt(self.staringAt.modelNode)
            return task.cont

        elif self.orbitType == "Cloud":
            if self.cloudClock < Orbiter.cloudTimer:
                self.cloudClock += 1

            else:
                self.cloudClock = 0
                positionVec = defensePaths.Cloud()
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

            self.modelNode.lookAt(self.staringAt.modelNode)
            return task.cont

class Consumable:
    def __init__(self, loader, render, name, position, scale=2.0):
        self.name = name
        self.modelNode = loader.loadModel('models/misc/sphere')  # built-in sphere
        self.modelNode.setColor(1.0, 0.4, 0.7, 1)  # pink (R, G, B, A)
        self.modelNode.setScale(scale)
        self.modelNode.reparentTo(render)
        self.modelNode.setPos(position)

        # Collision
        cNode = CollisionNode(name)
        cNode.addSolid(CollisionSphere(0, 0, 0, 1.5))  # Adjust radius if needed
        self.collisionNode = self.modelNode.attachNewNode(cNode)
        self.collisionNode.setTag("type", "consumable")

        self.collected = False

    def collect(self):
        self.collected = True
        self.modelNode.hide()

class Wanderer(SphereCollideObject):
    numWanderers = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, modelName: str,
                 scaleVec: float, texPath: str, staringAt, startPos=Vec3(0,0,0)):
        super().__init__(loader, modelPath, parentNode, nodeName, startPos, scaleVec, scaleVec)

        self.modelNode.setName(modelName)
        self.modelNode.setScale(scaleVec)

        self.collisionNode.setTag("type", "wanderer")

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.staringAt = staringAt

        Wanderer.numWanderers += 1
        intervalName = f"Traveler-{Wanderer.numWanderers}"

        p0 = Vec3(1000, 0, 0) + startPos
        p1 = Vec3(-500, 800, 0) + startPos
        p2 = Vec3(-500, -800, 0) + startPos

        posInterval0 = self.modelNode.posInterval(20, p0, startPos=startPos)
        posInterval1 = self.modelNode.posInterval(20, p1, startPos=p0)
        posInterval2 = self.modelNode.posInterval(20, p2, startPos=p1)

        self.travelRoute = Sequence(posInterval0, posInterval1, posInterval2, name=intervalName)

        self.travelRoute.loop()

