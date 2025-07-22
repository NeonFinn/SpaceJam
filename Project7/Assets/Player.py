import time

from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from panda3d.core import CollisionNode, CollisionSphere
import Classes as classesRef
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
        self.ambientSound.setVolume(0.1)
        self.ambientSound.play()

        # Load sound for missile
        self.fireSound = base.loader.loadSfx('Noise/missile.mp3')
        self.fireSound.setVolume(0.1)

        # Load sound for movement
        self.moveSound = base.loader.loadSfx('Noise/forward.mp3')
        self.moveSound.setLoop(True)
        self.moveSound.setVolume(1)
        self.moveSoundPlaying = False

        self.fireCooldown = 0.5
        self.originalFireCooldown = 2.0

        self.lastFireTime = 0

        self.speedMultiplier = 1.0
        self.fireRateBoost = False
        self.boostDuration = 0.0

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
        rate = 0.25 * self.getCamSlowMultiplier()

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
            if not self.moveSoundPlaying:
                self.moveSound.play()
                self.moveSoundPlaying = True
        else:
            if self.moveSoundPlaying:
                self.moveSound.stop()
                self.moveSoundPlaying = False

        if self.keys["fire"]:
            currentTime = time.time()

            # longer cooldown in fog
            cooldownMultiplier = 1.0
            if hasattr(self.base, "fogZone"):
                playerPos = self.modelNode.getPos()
                if self.base.fogZone.inside(playerPos):
                    cooldownMultiplier = 3.0  # 3x slower

            effectiveCooldown = self.fireCooldown * cooldownMultiplier
            if self.fireRateBoost:
                effectiveCooldown *= 0.25  # 75% faster fire rate

            currentTime = time.time()
            if currentTime - self.lastFireTime >= self.fireCooldown:
                self.fireMissile()
                self.lastFireTime = currentTime

            self.keys["fire"] = False

            if self.boostDuration > 0:
                self.boostDuration -= globalClock.getDt()
                if self.boostDuration <= 0:
                    self.speedMultiplier = 1.0
                    self.fireCooldown = self.originalFireCooldown  # back to normal
                    self.fireRateBoost = False

        return Task.cont

    def applyThrust(self):
        speed = 2 * self.speedMultiplier
        speedMultiplier = 1.0

        # Check if player is in fog zone and slow them and rotation down accordingly
        if hasattr(self.base, "fogZone"):
            playerPos = self.modelNode.getPos()
            if self.base.fogZone.inside(playerPos):
                speedMultiplier = 0.25

        trajectory = self.base.render.getRelativeVector(self.modelNode, Vec3(0, 1, 0))  # Forward is Y
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * speed * speedMultiplier)

    def getCamSlowMultiplier(self):
        camSlowMultiplier = 1.0
        if hasattr(self.base, "fogZone"):
            playerPos = self.modelNode.getPos()
            if self.base.fogZone.inside(playerPos):
                camSlowMultiplier = 0.25
        return camSlowMultiplier

    def fireMissile(self):
        if classesRef.Missile.missileBay > 0:
            aim = self.base.render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()

            fireSolution = aim * classesRef.Missile.missileDistance
            inFront = aim * 150

            travVec = fireSolution + self.modelNode.getPos()
            classesRef.Missile.missileBay -= 1
            tag = 'Missile' + str(classesRef.Missile.missileCount + 1)
            classesRef.Missile.missileCount += 1

            posVec = self.modelNode.getPos() + inFront
            currentMissile = classesRef.Missile(self.base.loader, 'Phaser/phaser.egg', self.base.render,
                                             tag, posVec, 4.0)

            classesRef.Missile.intervals[tag] = currentMissile.modelNode.posInterval(
                2.0, travVec, startPos=posVec, fluid=1)

            classesRef.Missile.intervals[tag].start()
            self.fireSound.play()
            self.isReloading = False

            self.traverser.addCollider(currentMissile.collisionNode, self.handler)

        else:
            if not self.taskMgr.hasTaskNamed('missileReload'):
                self.isReloading = False
                self.taskMgr.doMethodLater(0, self.reload, 'reload')

                return Task.cont

    def reload(self, task):
        if not self.isReloading:
            self.isReloading = True

        # Apply boost effect to reload time
        effectiveReloadTime = classesRef.Missile.reloadTime
        if self.fireRateBoost or self.boostDuration > 0:
            effectiveReloadTime *= 0.25  # 75% faster reload

        if task.time > effectiveReloadTime:
            if classesRef.Missile.missileBay < 1:
                classesRef.Missile.missileBay = 1
            self.isReloading = False
            return Task.done

        return Task.cont

    def checkIntervals(self, task):
        for i in classesRef.Missile.intervals:
            if not classesRef.Missile.intervals[i].isPlaying(): # Returns true or false to see if missile has reached path end
                classesRef.Missile.cNodes[i].detachNode()
                classesRef.Missile.fireModels[i].detachNode()

                del classesRef.Missile.intervals[i]
                del classesRef.Missile.fireModels[i]
                del classesRef.Missile.cNodes[i]
                del classesRef.Missile.collisionSolids[i]

                classesRef.Missile.missileBay += 1

                break # Refactoring to remove all intervals that have completed their path

        return Task.cont

    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        intoNode = entry.getIntoNodePath().getName()

        intoPosition = Vec3(entry.getSurfacePoint(self.base.render))

        tempVar = fromNode.split('_')
        shooter = tempVar[0]

        # Remove the '_cNode' suffix to get node name
        victim = intoNode.replace('_cNode', '')

        # Remove prefix and suffix to get base item type
        strippedString = re.sub(r'[0-9_]', '', victim)

        # Check if object is allowed to be destroyed
        if strippedString in ["Drone", "DroneX", "DroneY", "DroneZ", "BaseballSeam", "Planet", "SpaceStation"]:
            self.DestroyObject(victim, intoPosition)

            classesRef.Missile.intervals[shooter].finish()

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.base.render.find(f"**/{hitID}")
        if nodeID.isEmpty():
            return
        nodeID.detachNode()

        self.explodeNode.setPos(hitPosition)
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

    def applyPowerUpBoost(self, duration=5.0):
        self.speedMultiplier = 3.0
        self.fireCooldown = 0.5  # faster firing
        self.fireRateBoost = True
        self.boostDuration = duration

