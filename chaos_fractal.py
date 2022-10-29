import random
import manim as mn

class ChaosFractal(mn.Group):
    def __init__(
        self,
        *dots,
        start_point = None,
        active_color = mn.YELLOW,
        inactive_color = mn.BLUE,
        proportion = 0.5,
        dot_config = None,
        point_config = None,
        seed = None,
    ):
        

        self.active_color = active_color
        self.inactive_color = inactive_color
        self.proportion = proportion

        self.random = random.Random(seed)

        if dot_config is None:
            dot_config = {}

        self.dots = mn.VGroup(*[mn.Dot(dot, radius = 0.04, **dot_config) for dot in dots], z_index=1)

        if point_config is None:
            point_config = {}

        point_config.setdefault("stroke_width", 2)

        self.points = mn.Mobject1D(color=self.inactive_color, z_index=1, **point_config)

        if start_point is None:
            start_point = sum((self.random.random() * dot.get_center() for dot in self.dots), start=mn.ORIGIN)

        self.active_point = mn.Dot(start_point, radius=0.04, color=self.active_color, z_index=1, **dot_config)

        self.add(self.points, self.dots, self.active_point)

    def step(self):
        target = self.random.choice(self.dots).get_center()
        next_point = mn.interpolate(self.active_point.get_center(), target, self.proportion)

        self.points.add_points([self.active_point.get_center()])
        self.active_point.move_to(next_point)

        return self

    def animate_step(self, scene, *, wait=0.25, anim_time=0.5):
        anims = []

        old_dot = self.active_point.copy()
        scene.add(old_dot)

        target_lines = mn.VGroup(*[
            mn.Line(self.active_point, dot, stroke_width=2) for dot in self.dots
        ]).set_color(mn.GRAY)
        anims.append(mn.Create(target_lines))

        target_index = self.random.randrange(len(self.dots))
        target_line = target_lines[target_index].copy().set_stroke(mn.GREEN, width=3)
        anims.append(mn.Create(target_line))

        target = self.dots[target_index].get_center()
        active_point = self.active_point.get_center()
        next_point = mn.interpolate(active_point, target, self.proportion)

        next_line = mn.Line(active_point, next_point, stroke_width=3, color=mn.BLUE)
        anims.append(mn.Create(next_line))

        self.points.add_points([active_point])
        anims.append(self.active_point.animate.move_to(next_point))

        anims.append(mn.FadeOut(mn.VGroup(
            target_lines,
            target_line,
            next_line,
            old_dot,
        )))

        for anim in anims:
            scene.play(anim, run_time=anim_time)
            scene.wait(wait)

class Chaos(mn.Scene):
    def construct(self):
        shape = mn.RegularPolygon(n=3, radius=4)
        shape.move_to([0,0,0])
        fractal = ChaosFractal(*shape.get_vertices())
        i = mn.Tex("i = 9999")
        i.move_to([-4, 3, 0])
        count = mn.Tex("")
        count.next_to(i, mn.RIGHT)
        self.add(fractal)
        self.wait()
        self.animated_steps(fractal, 5)
        self.discrete_steps(fractal, 200, wait = 0.04, count = count, i = i)
        self.discrete_steps(fractal, 9800, wait = 0, count = count, i = i)
        self.play(mn.Create(i))
        self.wait()
        
        #self.discrete_steps(fractal, 100)
        
    def discrete_steps(self, fractal, n, *, wait=0.04, count, i):
        for _ in range(n):
            fractal.step()
            #count = mn.Tex(str(_))
            #count.next_to(i, mn.RIGHT)

            if(wait != 0):
                self.wait(wait)

    def animated_steps(self, fractal, n, **kwargs):
        for _ in range(n):
            fractal.animate_step(self, **kwargs)

