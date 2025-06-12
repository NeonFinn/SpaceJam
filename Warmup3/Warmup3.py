from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse() # disable mouse control
        self.camera.setPos(0.0, 0.0, 250.0) # top-down view
        self.camera.setHpr(0.0, -90.0, 0.0) # x, y, z axis rotation

        self.fighter = self.loader.loadModel('./Assets/sphere') # load the fighter model
        self.fighter.reparentTo(self.render) # add fighter to scene graph (makes it visible)
        self.fighter.setColorScale(1.0, 0.0, 0.0, 1.0) # set sphere color to red
        self.set_background_color(0,0,0) # set background color to black

        # add collision to fighter
        self.fighterCnode = self.fighter.attachNewNode(CollisionNode("fighterCnode")) # attach a new collision node to the fighter
        self.fighterCnode.node().addSolid(CollisionSphere(0, 0, 0, 1.8)) # add a collision sphere to the collision node
        self.fighterCnode.show() # show the collision sphere on fighter for debugging

        # setup collision system
        self.traverser = CollisionTraverser() # object that detects collisions
        self.traverser.traverse(self.render) # traverse the scene graph to find collisions
        self.pusher = CollisionHandlerPusher() # object that prevents overlapping by pushing objects apart
        self.pusher.addCollider(self.fighterCnode, self.fighter) # assign fighter collider to pusher, fighter is object to be pushed
        self.traverser.addCollider(self.fighterCnode, self.pusher) # add fighter collider to traverser with the pusher handler
        self.cTrav = self.traverser # assign traverser so panda3d can use it
        self.cTrav.showCollisions(self.render) # show where collisions are happening for debugging

        self.parent = self.loader.loadModel("./Assets/cube") # load the cube model

        x = 0  # initialize x
        for i in range(100):  # loop to create 100 cubes
            theta = x
            self.placeholder2 = self.render.attachNewNode('Placeholder2')  # put placeholder in renderer
            self.placeholder2.setPos(
                50.0 * math.cos(theta),  # x position
                50.0 * math.sin(theta),  # y position
                0.0                      # z position
            )

            red = 0.6 + random.random() * 0.4  # randomize colors
            green = 0.6 + random.random() * 0.4
            blue = 0.6 + random.random() * 0.4
            self.placeholder2.setColorScale(red, green, blue, 1.0)  # set color scale of placeholder2

            self.parent.instanceTo(self.placeholder2) # take cube and instance to placeholder2

            # add a collision node to each cube instance
            cnode = self.placeholder2.attachNewNode(CollisionNode("pcnode")) # each cube has its own collision node, reusing was causing it to appear choppy
            cnode.node().addSolid(CollisionSphere(0, 0, 0, 1.8)) # add a collision sphere to the collision node
            cnode.show() # show the collision sphere on cubes for debugging

            x = x + 0.06 # adds space between cubes

        self.accept('escape', self.quit)  # if escape is pressed quit

        self.accept('a', self.negativeX, [1])  # right
        self.accept('a-up', self.negativeX, [0])

        self.accept('d', self.positiveX, [1])  # left
        self.accept('d-up', self.positiveX, [0])

        self.accept('s', self.negativeY, [1])  # down
        self.accept('s-up', self.negativeY, [0])

        self.accept('w', self.positiveY, [1])  # up
        self.accept('w-up', self.positiveY, [0])

    # functions to move fighter when called
    def movePositiveX(self, task):
        self.fighter.setX(self.fighter, 0.5)
        return task.cont

    def moveNegativeX(self, task):
        self.fighter.setX(self.fighter, -0.5)
        return task.cont

    def movePositiveY(self, task):
        self.fighter.setY(self.fighter, 0.5)
        return task.cont

    def moveNegativeY(self, task):
        self.fighter.setY(self.fighter, -0.5)
        return task.cont

    # if key is pressed, add task to move fighter, if key is released, remove task
    def positiveX(self, keyDown):
        if (keyDown):
            self.taskMgr.add(self.movePositiveX, "movePositiveX")
        else:
            self.taskMgr.remove("movePositiveX")

    def negativeX(self, keyDown):
        if (keyDown):
            self.taskMgr.add(self.moveNegativeX, "moveNegativeX")
        else:
            self.taskMgr.remove("moveNegativeX")

    def positiveY(self, keyDown):
        if (keyDown):
                self.taskMgr.add(self.movePositiveY, "movePositiveY")
        else:
            self.taskMgr.remove("movePositiveY")

    def negativeY(self, keyDown):
        if (keyDown):
            self.taskMgr.add(self.moveNegativeY, "moveNegativeY")
        else:
            self.taskMgr.remove("moveNegativeY")

    def quit(self): # function to quit application
        sys.exit()

app = MyApp() # create instance of MyApp
app.run() # run application