from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from panda3d.core import CollisionNode, CollisionSphere
from Project5.Assets import Classes


class player:
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable, modelPath: str, parentNode: NodePath,
                 nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, base):

        self.taskMgr = taskMgr
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
            "rollRight": False,
            "fire": False
        }

        self.setKeyBinds()
        self.base.taskMgr.add(self.updatePlayer, "updatePlayer")
        self.taskMgr.add(self.checkIntervals, 'checkMissiles', 34)

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
        self.base.accept("f", self.setKey, ["fire", True])

    def updatePlayer(self, task):
        rate = 0.25
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
        if self.keys["fire"]:
            self.fireMissile()
            self.keys["fire"] = False  # Reset fire key to prevent multiple firings

        return Task.cont

    def applyThrust(self):
        rate = 2
        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3(0, 1, 0))  # Forward is Y
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

    def fireMissile(self):
        if Classes.Missile.missileBay > 0:
            aim = self.base.render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()

            fireSolution = aim * Classes.Missile.missileDistance
            inFront = aim * 150

            travVec = fireSolution + self.modelNode.getPos()
            Classes.Missile.missileBay -= 1
            tag = 'Missile' + str(Classes.Missile.missileCount + 1)
            Classes.Missile.missileCount += 1

            posVec = self.modelNode.getPos() + inFront
            currentMissile = Classes.Missile(self.base.loader, 'Phaser/phaser.egg', self.base.render,
                                             tag, posVec, 4.0)

            Classes.Missile.intervals[tag] = currentMissile.modelNode.posInterval(
                2.0, travVec, startPos=posVec, fluid=1)

            Classes.Missile.intervals[tag].start()

            self.isReloading = False

        else:
            if not self.taskMgr.hasTaskNamed('missileReload'):
                print('Initializing reload...')
                self.isReloading = False
                self.taskMgr.doMethodLater(0, self.reload, 'reload')

                return Task.cont

    def reload(self, task):
        if not self.isReloading:
            print('Reloading...')  # print once at the start
            self.isReloading = True

        if task.time > Classes.Missile.reloadTime:
            if Classes.Missile.missileBay > 1:
                Classes.Missile.missileBay = 1
            print('Reload complete.')
            self.isReloading = False
            return Task.done

        return Task.cont

    def checkIntervals(self, task):
        for i in Classes.Missile.intervals:
            if not Classes.Missile.intervals[i].isPlaying(): # returns true or false to see if missile has reached path end
                Classes.Missile.cNodes[i].detachNode()
                Classes.Missile.fireModels[i].detachNode()

                del Classes.Missile.intervals[i]
                del Classes.Missile.fireModels[i]
                del Classes.Missile.cNodes[i]
                del Classes.Missile.collisionSolids[i]

                Classes.Missile.missileBay += 1
                print(i + ' has reached the end of its fire solution.')

                break # refactoring to remove all intervals that have completed their fire solution

        return Task.cont