import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import Window


import sys
sys.path.append('modules')
 

from collide import *
from Logger import *
from PointReader import *

  

# load our images
block = pyglet.resource.image('images/block.png')

folder = 'images/'

#imageToAnalyze = ('world.png')
imageToAnalyze = ('circle.png')
#imageToAnalyze = ('pieces.png')
#imageToAnalyze = ('yellow_world.png')
#imageToAnalyze = ('constellation_north.png')
#imageToAnalyze = ('me.png')


#world = pyglet.resource.image('images/world.png')
#world = pyglet.resource.image('images/yellow_world.png')
world = pyglet.resource.image(folder + imageToAnalyze)

MAXWIDTH  =  world.width
MAXHEIGHT =  world.height

MINWIDTH  =  block.width/2
MINHEIGHT =  block.height/2

WINDOWBORDER = 20


# create a simple window
window = pyglet.window.Window(MAXWIDTH, MAXHEIGHT, caption="Scan image (press up,down,right,left)", visible=False)

# create the render structures
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0) 
foreground = pyglet.graphics.OrderedGroup(1)

step = 1

class Entity(pyglet.sprite.Sprite):
	'''Movable, collidable entity class'''
	
	def __init__(self, image, x, y, batch, group, direction=""):
		pyglet.sprite.Sprite.__init__(self, image, x, y, batch=batch, group=group)
		
		# create a collision structure for this sprite
		self.collision = SpriteCollision(self)
		
		# stay alive for 4 seconds
		self.life = 4.0
		self.direction = direction
 

# create the level as an entity
level = Entity(world, 0, 0, batch, background)

# create a set to contain the blocks
# a set has a very fast difference operation,
# which we will use in the update function
blocks = set()

all = set()


@window.event
def on_mouse_press(x, y, button, modifiers):

	#button 4 add automatically blocks
	if (button==4):
		autoPutBlocks("UP")
	else:
		'''Create a new block whenever the user clicks the mouse'''	
	# create a new block
		b = Entity(block, x, y, batch, foreground)
		# add it to the set
		blocks.add(b)
		all.add(b)

@window.event
def on_key_press(symbol, modifiers):
  if symbol == key.UP:
      print 'The up was pressed.'
      autoPutBlocks("UP")
  elif symbol == key.DOWN:
      print 'The down was pressed.'
      autoPutBlocks("DOWN")
  elif symbol == key.LEFT:
      print 'The left was pressed.'
      autoPutBlocks("LEFT")
  elif symbol == key.RIGHT:
      print 'The right was pressed.'
      autoPutBlocks("RIGHT")
            


@window.event
def on_draw():
	# clear the window
	window.clear()
	
	# draw our background and blocks
	batch.draw()

def update(dt):
	# we need to set the blocks variable, so declare it global
	global blocks
	global lastB
	global lastBatch
	#lastB = None

	lastBatch = True
 
	for index, b in enumerate(blocks):

		if index == 0:
			print 'x : ' , b.x, ' y: ' , b.y

		if b.direction == "DOWN":
			if b.y < 0:
				b.y = 0
			b.y -= MINHEIGHT

			while collide(b.collision, level.collision):
				b.y += 1

		elif b.direction == "UP":
			if b.y > window.height-WINDOWBORDER:
				b.y = window.height

			b.y += MINHEIGHT

			while collide(b.collision, level.collision):
				b.y -= 1

		elif b.direction == "LEFT":
			if b.x < 0:
				b.x = 0
			b.x -= MINHEIGHT

			while collide(b.collision, level.collision):
				b.x += 1

		elif b.direction == "RIGHT":
			if b.x > window.width:
				b.x = window.width

			b.x += MINHEIGHT

			while collide(b.collision, level.collision):
				b.x -= 1


		b.life -= 1/30.0
 
	# use a generator expression to construct a new set containing only the dead blocks
	dead = set(b for b in blocks if b.life <= 0.0)
	
	# remove the dead blocks from the render batch
	for index, b in enumerate(dead): 
		b.batch = None
 
	if len(dead) == len(blocks):
		lastBatch = False
 
	
	# use a set difference operation to remove the dead blocks from the update set
	blocks = blocks.difference(dead)


def autoPutBlocks(direction):
  
  #every time, blocks moves of a step
  global step
  
  #step = 0
  
  h = window.height
  w = window.width
  

  section = 20  
  
  if not lastBatch:
	  for i in range(0,w,w/(section)+step):
	    if direction == "DOWN" :  
	      b = Entity(block, i, h-WINDOWBORDER, batch, foreground,direction)
	    elif direction == "UP":  
	      b = Entity(block, i, 0, batch, foreground,direction)
	    elif direction == "LEFT":  
	      b = Entity(block, w, i, batch, foreground,direction)
	    elif direction == "RIGHT":  
	      b = Entity(block, 0, i, batch, foreground,direction)      
	  # add it to the set
	    blocks.add(b)
	    all.add(b)

	  step+=1 


def main():


  #if (!image):
  #  image = dummyImage
  
  glClearColor(1.0, 1.0, 1.0, 1.0)
  window.clear()
  window.flip()

  # make the window visible
  window.set_visible(True)

  # schedule our update function
  pyglet.clock.schedule_interval(update, 1/30.0)
  #pyglet.clock.schedule_interval(scan, 1/30.0)
  

  # and finally, run the app...
  pyglet.app.run()

  
  #l = Logger("","collision.log",".")
  now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  
  logFolder = "logs"
  logFile = imageToAnalyze + "_" + now + ".log"
  
  for index,elem in enumerate(all): 
    if elem.x > MINWIDTH and elem.x < MAXWIDTH and elem.y < MAXHEIGHT and elem.y > MINHEIGHT:
      data = str(index) + " [" + str(elem.x) + "," + str(elem.y) + "]"
      #print data #index , " [" , elem.x , "," , elem.y , "]"
      
      #l = Logger(data,"collision.log",".")
    
      l = Logger(data,logFile,logFolder)
  
  
  return logFolder + '\\' + logFile
      
log = main()
print "opening " + log 
PR = PointReader("", log)
