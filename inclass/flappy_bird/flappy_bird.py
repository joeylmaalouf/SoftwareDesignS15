""" A Flappy Bird Clone Starring the Olin O """

import pygame
import random
import time

class FlappyModel(object):
    """ Represents the game state of our Flappy bird clone.

        The tracks the background (which consists of the ground as well as
        the stars), the location of the Bird (the Olin "O"), and the pipe
        obstacles.

        All of the items in the model implement a get_drawables function that
        returns a list of DrawableSurface objects.  Each DrawableSurface contains
        a surface (which defines the appearance of the object) and a rect which
        defines where the object should be drawn.  The coordinates of the rects
        are defined with respect to a coordinate system with the origin placed
        in the upper lefthand corner of the very beginning of the FlappyBird
        level.  It is the responsibility of the view to draw the rects at the
        appropriate location on the screen (which only encompasses a small
        fraction of the level.
    """
    def __init__(self, width, height):
        """ Initialize the flappy model.  """
        self.width = width
        self.height = height
        self.bird = Bird(0, height/2.0)
        self.background = Background(width, height)
        self.obstacles = []
        # create 100 PipeObstacles spaced by 500 pixels.
        for i in range(100):
            self.obstacles.append(PipeObstacle((i+1)*500, height))

    def get_drawables(self):
        """ Return a list of DrawableSurfaces for the model. """
        drawables = self.background.get_drawables()+self.bird.get_drawables()
        for obstacle in self.obstacles:
            drawables += obstacle.get_drawables()
        return drawables

    def is_dead(self):
        """ Return True if the player is dead (for instance) the player
            has collided with an obstacle, and false otherwise """
        # TODO: modify this if the player becomes more complicated
        player_rect = self.bird.get_bounding_rect()
        if self.background.collided_with(player_rect):
            return True
        for obstacle in self.obstacles:
            if obstacle.collided_with(player_rect):
                return True
        return False

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.bird.update(delta_t)

class DrawableSurface(object):
    """ A class that wraps a pygame.Surface and a pygame.Rect """
    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

class Background():
    """ Represents the contents of the background """
    def __init__(self, screen_width, screen_height):
        """ initialize the background for Flappy Bird.  The variables
            screen_width and screen_height are the size of the
            screen in pixels """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile = pygame.image.load('images/plant_tile.png')
        self.tile.set_colorkey((255,255,255))
        self.star = pygame.image.load('images/largeyellowstar.jpg')
        # rescale the star since to 1/10th original size since it is too large
        w,h = self.star.get_size()
        self.star = pygame.transform.scale(self.star, (int(0.1*w), int(0.1*h)))
        self.star.set_colorkey((255,255,255))

        self.star_x = []
        self.star_y = []
        """ randomly put 1000 stars in the sky.  Currently we are distributing the
            stars randomly from x position 0 to x position 25000.  This means that
            if you went far enough in the level, the stars would stop showing up.
            ideally you would want to end the level at that point. """
        for i in range(1000):
            self.star_x.append(random.randint(0,25000))
            self.star_y.append(random.randint(0,screen_height-100))

    def get_drawables(self):
        """ Get the drawables for the background """
        drawables = []
        # first synthesize the star drawables then get the ground
        # drawables in a separate method.
        for i in range(len(self.star_x)):
            r = pygame.Rect(self.star_x[i],
                            self.star_y[i],
                            self.star_x[i] + self.star.get_rect().width,
                            self.star_y[i] + self.star.get_rect().height)
            drawables.append(DrawableSurface(self.star, r))
        return drawables + self.get_ground_drawables()

    def get_ground_drawables(self):
        """ Get just the drawables that are part of the ground.  These
            have been separated out since death will only occur if there
            is a collision with the ground (rather than the stars for instance """
        drawables = []
        # create the initial rectangle at the lower left corner of the beginning
        # of the level
        r = pygame.Rect(0,
                        self.screen_height-self.tile.get_rect().height,
                        self.tile.get_rect().width,
                        self.tile.get_rect().height)
        for i in range(1000):
            # store the DrawableSurface in the list
            drawables.append(DrawableSurface(self.tile,r))
            """ move the rectangle over as many pixels as the image is wide so
                that a new DrawableSurface can be created for the next image
                tile that composes the floor.  Since we are only doing this
                1000 times the ground will eventually stop appearing.  It would
                probably be a good idea to stop the level at that point. """
            r = r.move(self.tile.get_rect().width,0)
        return drawables

    def collided_with(self, entity_rect):
        """ Returns True if and only if the input rectangle entity_rect
            has collided with the ground and false otherwise """
        # the ground drawables define both the appearance of the ground tiles
        # and also their position.  This allows us to use pygame's collidelist
        # feature to test for a collision (see below)
        drawables = self.get_ground_drawables()
        rectangles = []
        for d in drawables:
            rectangles.append(d.rect)
        # use pygame's built-in collision detection to see if the input rectangle
        # entity_rect has collided with any rectangle that composes the ground.
        # the code -1 referenced below means no collision has occurred.
        return entity_rect.collidelist(rectangles) != -1

class Bird(object):
    """ Represents the player in the game (the Flappy Bird) """
    def __init__(self, pos_x, pos_y):
        """ Initialize a Flappy bird at position (pos_x, pos_y) """
        self.pos_x = pos_x
        self.pos_y = pos_y
        # start with a x velocity of 50 pixels per second
        self.v_x = 50
        # start with 0 y velocity
        self.v_y = 0
        # TODO: don't depend on relative path (you don't really want to hardcode
        # this path).
        self.image = pygame.image.load('images/olin_o.png')
        self.image.set_colorkey((255,255,255))

    def get_bounding_rect(self):
        """ Returns a rectangle that encompasses the player (Flappy Bird).  This
            rectangle is used primarily to detect when the player has died. """
        return self.get_drawables()[0].rect

    def get_drawables(self):
        """ Fet the drawables that makeup the FlappyBird Player.  Currently there
            is just one (the image of the Olin O) """
        return [DrawableSurface(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))]

    def update(self, delta_t):
        """ update the flappy bird's position """
        self.pos_x += self.v_x*delta_t
        self.pos_y += self.v_y*delta_t
        self.v_y += delta_t*100 # this is gravity in pixels / s^2

    def flap(self):
        """ cause the bird to accelerate upwards (negative y direction) """
        self.v_y -= 100

class PipeObstacle():
    """ A class that represents a double pipe obstacle """
    def __init__(self, pos_x, screen_height):
        """ Initialize a pip obstacle at the specified x coordinate pos_x """
        self.pos_x = pos_x
        # choose the location y coordinate of the upward facing (bottom) pipe
        self.pos_y_bottom = random.randint(100,screen_height-100)
        # the y coordinate of the downward facing (top) pipe is always 200 pixels
        # away from the upward facing pipe
        self.pos_y_top = self.pos_y_bottom - 200
        self.screen_height = screen_height
        # pipe_top and pipe_body are the two images used draw the pipe obstacle
        self.pipe_top = pygame.image.load('images/pipe_top.png')
        self.pipe_body = pygame.image.load('images/pipe_body.png')
        # the images must be rescaled by a factor of 0.5 since they are too large
        w,h = self.pipe_top.get_size()
        self.pipe_top = pygame.transform.scale(self.pipe_top, (int(w*0.5),int(h*0.5)))
        w,h = self.pipe_body.get_size()
        self.pipe_body = pygame.transform.scale(self.pipe_body, (int(w*0.5),int(h*0.5)))
        # we also store a flipped version fo the pipe top for drawing the downward
        # facing pipe
        self.pipe_top_flipped = pygame.transform.flip(self.pipe_top, False, True)

    def get_drawables(self):
        """ Get the drawables that constitute a pipe obstacle """
        drawables = []
        # add the drawable for the top of the upward facing pipe
        r = pygame.Rect(self.pos_x,
                        self.pos_y_bottom,
                        self.pipe_top.get_rect().width,
                        self.pipe_top.get_rect().height)
        drawables.append(DrawableSurface(self.pipe_top,r))

        # move the pipe down so we are ready to create the drawable
        # corresponding to the pipe body
        r = r.move(0,self.pipe_top.get_rect().height)
        while r.top <= self.screen_height:
            # add a drawable for the pipe body of the upward facing pipe
            drawables.append(DrawableSurface(self.pipe_body,r))
            # move the rectangel so we are ready to add another segment
            # of the pipe body
            r = r.move(0,self.pipe_body.get_rect().height)

        # add the drawables for the downward facing pipe
        r = pygame.Rect(self.pos_x,
                        self.pos_y_top,
                        self.pipe_top_flipped.get_rect().width,
                        self.pipe_top_flipped.get_rect().height)
        # use the flipped top image since this pipe is upside down
        drawables.append(DrawableSurface(self.pipe_top_flipped,r))

        while r.top > -self.pipe_body.get_rect().height:
            # move the rectangle so we can add the next pipe body segment
            # of the downward facing pipe
            r = r.move(0,-self.pipe_body.get_rect().height)
            drawables.append(DrawableSurface(self.pipe_body,r))
        return drawables

    def collided_with(self, entity_rect):
        """ Returns true if and only if the input rectangle entity_rect
            has collided with the obstacle """
        drawables = self.get_drawables()
        rectangles = []
        for d in drawables:
            rectangles.append(d.rect)
        return entity_rect.collidelist(rectangles) != -1

class FlappyView(object):
    """ The view of the Flappy Bird game.  This renders the Flappy Bird game
        state in a Pygame window """
    def __init__(self, model, width, height):
        """ Initialize the view for Flappy Bird.  The input model
            is necessary to find the position of relevant objects to draw. """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # the current screen boundaries
        self.screen_boundaries = pygame.Rect(0 ,0, width, height)
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        # paint the screen a midnight blue
        self.screen.fill((0,51,102))
        # get the new drawables
        self.drawables = self.model.get_drawables()
        # move the screen boundaries to coincide with the player's x coordinate
        screen_position = self.screen_boundaries.move(self.model.bird.pos_x,0)
        for d in self.drawables:
            """ the coordinates of the drawables are defined relative to an origin
                placed in the upper left corner of the beginning of the level.  In
                order to render them within the current screen boundaries, we need
                to shift them over based on the screen's position. """
            rect = d.rect.move(-screen_position.x, -screen_position.y)
            self.screen.blit(d.surface, rect)
        pygame.display.update()

class PygameKeyboardController():
    """ Controls flappy bird by mapping spacebar to upward acceleration """
    def __init__(self, model):
        """ initialize the keyboard controller.  The specified model
            will be manipulated in response to user key presses """
        self.model = model
        self.space_pressed = False

    def process_events(self):
        """ process keyboard events.  This must be called periodically
            in order for the controller to have any effect on the game """
        pygame.event.pump()
        if not(pygame.key.get_pressed()[pygame.K_SPACE]):
            self.space_pressed = False
        elif not(self.space_pressed):
            self.space_pressed = True
            self.model.bird.flap()

class FlappyBird():
    """ The main Flappy Bird class """

    def __init__(self):
        """ Initialize the flappy bird game.  Use FlappyBird.run to
            start the game """
        self.model = FlappyModel(640, 480)
        self.view = FlappyView(self.model, 640, 480)
        self.controller = PygameKeyboardController(self.model)

    def run(self):
        """ the main runloop... loop until death """
        last_update_time = time.time()
        while not(self.model.is_dead()):
            # redraw the level
            self.view.draw()
            # check for key presses
            self.controller.process_events()
            # compute delta_t so we know how much to update various
            # positions in in the model.update function.
            delta_t = time.time() - last_update_time
            # update the model (basically runs the physics of the game)
            self.model.update(delta_t)
            # store the last update time so we can calculate the next delta_t
            last_update_time = time.time()

if __name__ == '__main__':
    flappy = FlappyBird()
    flappy.run()