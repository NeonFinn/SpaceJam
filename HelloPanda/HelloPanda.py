from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.scene = self.loader.loadModel("models/environment") # load environment model
        self.scene.reparentTo(self.render) # re-parent to the renderer
        self.scene.setScale(0.25, 0.25, 0.25) # scale model
        self.scene.setPos(-8, 42, 0) # set position of model

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask") # add task to spin camera

        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"}) # load panda model and animation
        self.pandaActor.setScale(0.005, 0.005, 0.005) # scale panda model
        self.pandaActor.reparentTo(self.render) # re-parent to the renderer
        self.pandaActor.loop("walk") # loop the walk animation

        # create four intervals that allow the panda to walk back and forth
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0)) # move panda from (0, 10, 0) to (0, -10, 0)
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0)) # move panda from (0, -10, 0) to (0, 10, 0)
        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0)) # rotate panda from (0, 0, 0) to (180, 0, 0)
        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0)) # rotate panda from (180, 0, 0) to (0, 0, 0)

        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace") # create sequence of intervals
        self.pandaPace.loop() # loop the sequence

    def spinCameraTask(self, task): # task to spin the camera around the panda
        angleDegrees = task.time * 6.0 # 6 degrees per second
        angleRadians = angleDegrees * (pi / 180.0) # convert degrees to radians
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3) # set camera position in a circular path
        self.camera.setHpr(angleDegrees, 0, 0) # set camera to face panda
        return Task.cont

app = MyApp() # create instance of MyApp
app.run() # run application