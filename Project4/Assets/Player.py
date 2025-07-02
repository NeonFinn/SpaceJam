from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from panda3d.core import CollisionNode, CollisionSphere


class player:
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable, modelPath: str, parentNode: NodePath,
                 nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, base):

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.collisionNode.show()

        self.base = base
        self.keys = {
            "forward": False,
            "turnLeft": False,
            "turnRight": False,
            "turnDown": False,
            "turnUp": False,
            "rollLeft": False,
            "rollRight": False
        }

        self.setKeyBinds()
        self.base.taskMgr.add(self.updatePlayer, "updatePlayer")

    def setKey(self, key, value):
        self.keys[key] = value

    def setKeyBinds(self):
        self.base.accept("space", self.setKey, ["forward", True])
        self.base.accept("space-up", self.setKey, ["forward", False])
        self.base.accept("a", self.setKey, ["turnLeft", True])
        self.base.accept("a-up", self.setKey, ["turnLeft", False])
        self.base.accept("d", self.setKey, ["turnRight", True])
        self.base.accept("d-up", self.setKey, ["turnRight", False])
        self.base.accept("s", self.setKey, ["turnDown", True])
        self.base.accept("s-up", self.setKey, ["turnDown", False])
        self.base.accept("w", self.setKey, ["turnUp", True])
        self.base.accept("w-up", self.setKey, ["turnUp", False])
        self.base.accept("q", self.setKey, ["rollLeft", True])
        self.base.accept("q-up", self.setKey, ["rollLeft", False])
        self.base.accept("e", self.setKey, ["rollRight", True])
        self.base.accept("e-up", self.setKey, ["rollRight", False])

    def updatePlayer(self, task):
        rate = 0.5
        if self.keys["turnLeft"]:
            self.modelNode.setH(self.modelNode.getH() + rate)
        if self.keys["turnRight"]:
            self.modelNode.setH(self.modelNode.getH() - rate)
        if self.keys["turnDown"]:
            self.modelNode.setP(self.modelNode.getP() - rate)
        if self.keys["turnUp"]:
            self.modelNode.setP(self.modelNode.getP() + rate)
        if self.keys["rollLeft"]:
            self.modelNode.setR(self.modelNode.getR() - rate)
        if self.keys["rollRight"]:
            self.modelNode.setR(self.modelNode.getR() + rate)
        if self.keys["forward"]:
            self.applyThrust()

        return Task.cont

    def applyThrust(self):
        rate = 5
        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3(0, 1, 0))  # Forward is Y
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)