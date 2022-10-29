from manim import *
import random
class Dot3DExample(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(distance=10, phi=75*DEGREES, theta=-85*DEGREES) #theta=-45*DEGREES

        axes = ThreeDAxes()
        axes.move_to([0, 0, 0])
        #start with 4 dots
        dot_1 = Dot3D(point=axes.coords_to_point(0, 4, 0), radius = 0.05, color=BLUE)
        dot_2 = Dot3D(point=axes.coords_to_point(4, -4, 0), radius = 0.05, color=BLUE)
        dot_3 = Dot3D(point=axes.coords_to_point(-4, -4, 0), radius = 0.05, color=BLUE)
        dot_4 = Dot3D(point=axes.coords_to_point(0, 0, 6), radius = 0.05, color=BLUE)
        dots = [dot_1, dot_2, dot_3, dot_4]
        #this is the current location of the "pen"
        curr = Dot3D(radius = 0.02, color = YELLOW)
        points = Mobject2D(radius = 0.01)
        self.add(axes, dot_1, dot_2,dot_3, dot_4, curr, points)
        self.begin_ambient_camera_rotation(rate = 0.1)
        for i in range(20000):
            a = random.choice(dots) #pick a random dot from the starting 4 dots
            #move halfway from the current location to the random dot
            next_point = interpolate(curr.get_center(), a.get_center(), 0.5)
            curr.move_to(next_point)
            #draw a new point there
            points.add_points([curr.get_center()])
        self.interactive_embed()
        self.wait(7)
        self.stop_ambient_camera_rotation()
            
        
        #self.wait(7)