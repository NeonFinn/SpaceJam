from direct.showbase.ShowBase import ShowBase
import math, sys, random

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.fighter = self.loader.loadModel('./Assets/sphere') # load the fighter model
        self.fighter.reparentTo(self.render) # re-parent to the renderer
        self.fighter.setColorScale(1.0, 0.0, 0.0, 1.0) # set sphere color to red
        self.set_background_color(0,0,0) # set background color to black

        self.accept('escape', self.quit) # if escape is pressed quit

        self.parent = self.loader.loadModel("./Assets/cube") # load the cube model

        x = 0 # use position of circle as center
        for i in range(100): # loop to create 100 cubes
            theta = x
            self.placeholder2 = self.render.attachNewNode('Placeholder2') # put in the renderer
            self.placeholder2.setPos(50.0 * math.cos(theta), 50.0 * math.sin(theta), 0.0 * math.tan(theta)) # create circle of cubes

            red = 0.6 + random.random() * 0.4 # randomize colors
            green = 0.6 + random.random() * 0.4
            blue = 0.6 + random.random() * 0.4

            self.placeholder2.setColorScale(red, green, blue, 1.0)  # set color scale of placeholder2

            self.parent.instanceTo(self.placeholder2) # take cube and instance to placeholder2
            x = x + 0.06 # adds space between cubes

    def quit(self): # function to quit application
        sys.exit()

app = MyApp() # create instance of MyApp
app.run() # run application