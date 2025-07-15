from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from panda3d.core import CollisionNode, CollisionSphere
from Project5.Assets import Classes
from panda3d.core import CollisionHandlerEvent
from direct.particles.ParticleEffect import ParticleEffect
import re

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

        self.cntExplode = 0
        self.explodeIntervals = {}

        self.traverser = base.cTrav

        self.handler = CollisionHandlerEvent()

        self.handler.addInPattern('into')
        accept('into', self.HandleInto)

        self.base = base

        self.SetParticles()

        # Load and loop space noise continuously
        self.ambientSound = base.loader.loadSfx('Noise/ambient.mp3')
        self.ambientSound.setLoop(True)
        self.ambientSound.setVolume(0.01)
        self.ambientSound.play()

        # Load sound for missile
        self.fireSound = base.loader.loadSfx('Noise/missile.mp3')
        self.fireSound.setVolume(0.1)

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
            self.keys["fire"] = False  # Reset fire key so it doesn't keep firing

        return Task.cont

    def applyThrust(self):
        base_speed = 2
        speedMultiplier = 1.0

        # Check if player is in fog zone and slow them down accordingly
        if hasattr(self.base, "fogZone"):
            playerPos = self.modelNode.getPos()
            if self.base.fogZone.inside(playerPos):
                speedMultiplier = 0.4

        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3(0, 1, 0))  # Forward is Y
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * base_speed * speedMultiplier)

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
            self.fireSound.play()
            self.isReloading = False

            self.traverser.addCollider(currentMissile.collisionNode, self.handler)

        else:
            if not self.taskMgr.hasTaskNamed('missileReload'):
                print('Initializing reload...')
                self.isReloading = False
                self.taskMgr.doMethodLater(0, self.reload, 'reload')

                return Task.cont

    def reload(self, task):
        if not self.isReloading:
            print('Reloading...')
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
            if not Classes.Missile.intervals[i].isPlaying(): # Returns true or false to see if missile has reached path end
                Classes.Missile.cNodes[i].detachNode()
                Classes.Missile.fireModels[i].detachNode()

                del Classes.Missile.intervals[i]
                del Classes.Missile.fireModels[i]
                del Classes.Missile.cNodes[i]
                del Classes.Missile.collisionSolids[i]

                Classes.Missile.missileBay += 1
                print(i + ' has reached the end of its fire solution.')

                break # Refactoring to remove all intervals that have completed their path

        return Task.cont

    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)

        intoPosition = Vec3(entry.getSurfacePoint(self.base.render))

        tempVar = fromNode.split('_')
        shooter = tempVar[0]
        print("Shooter: " + str(shooter))

        # Remove the '_cNode' suffix to get node name
        victim = intoNode.replace('_cNode', '')
        print("Victim: " + victim)

        # Remove prefix and suffix to get base item type
        strippedString = re.sub(r'[0-9_]', '', victim)

        # Check if object is allowed to be destroyed
        if strippedString in ["Drone", "DroneX", "DroneY", "DroneZ", "BaseballSeam", "Planet", "SpaceStation"]:
            print(victim, 'hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)

            print(shooter + ' is DONE.')
            Classes.Missile.intervals[shooter].finish()

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.base.render.find(f"**/{hitID}")
        if nodeID.isEmpty():
            return
        nodeID.detachNode()

        self.explodeNode.setPos(hitPosition)
        print(f"Explosion position: {hitPosition}")
        self.Explode(hitPosition)

    def Explode(self, position):
        cnt = self.cntExplode
        self.cntExplode += 1
        tag = f'Explosion-{cnt}'

        # Create a new node for explosion
        explodeNode = self.base.render.attachNewNode(tag)
        explodeNode.setPos(position)

        # Create a new ParticleEffect instance and load
        effect = ParticleEffect()
        effect.loadConfig('Part-Fx/Part-Efx/basic_xpld_efx.ptf')
        effect.setScale(50)
        effect.start(explodeNode)

        # Reset particles to emit instantly
        effect.softStart()

        # Clean up after 4 seconds
        def cleanupExplosion(task):
            effect.cleanup()
            explodeNode.removeNode()
            return Task.done

        self.taskMgr.doMethodLater(4.0, cleanupExplosion, f'{tag}-cleanup')

    def ExplodeLight(self, t):
        if t == 0.00:
            self.explodeEffect.start(self.explodeNode)
        elif t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()

    def SetParticles(self):
        self.enableParticles = True
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig('Part-Fx/Part-Efx/basic_xpld_efx.ptf')
        self.explodeEffect.setScale(100)
        self.explodeNode = self.base.render.attachNewNode('ExplosionEffect')

        self.explodeEffect.reparentTo(self.explodeNode)