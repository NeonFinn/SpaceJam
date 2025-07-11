from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task

from CollideObjectBase import *

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

        self.collisionNode.show()

        print("Fire torpedo #" + str(Missile.missileCount))