from dataclasses import dataclass
import os
from manim import *
import sys
import numpy as np
import random

script_dir = os.path.dirname(os.path.realpath(__file__))
def local_path(path: str) -> str:
    return os.path.join(script_dir, path)

monospace = "Monospace"
if sys.platform == 'win32':
    monospace = 'consolas'
elif sys.platform == 'darwin':
    monospace = 'monaco'


class Intro(Scene):
    def construct(self):
        p = MathTex(r'x^2 - x - 2 = 0').shift(UP)
        self.play(Write(p))
        p_factor = MathTex(r'(x - 2)(x + 1) = 0').next_to(p, direction=DOWN)
        self.play(Write(p_factor))
        p_complete = MathTex(r'\left(x - \frac{1}{2}\right)^2 - \frac{9}{4} = 0').next_to(p_factor, direction=DOWN)
        self.play(Write(p_complete))
        p_formula = MathTex(r'x = \frac{1 \pm \sqrt{1+8}}{2}').next_to(p_complete, direction=DOWN)
        self.play(Write(p_formula))
        self.play([Unwrite(mob) for mob in [p, p_factor, p_complete, p_formula]])
        
        # (x - 1)(x - 2)(x + 1)
        p_cubic = MathTex(r'x^3 - 2x^2 - x + 2')
        self.play(Write(p_cubic))
        # TODO cubic equation, at least an image
        # TODO show vomit emoji
        self.play(Unwrite(p_cubic))

        # that * (x + 4)
        p_quartic = MathTex(r'x^4 + 2x^3 - 9x^2 - 2x + 8')
        self.play(Write(p_quartic))
        # TODO show picture of quartic formula
        self.play(Unwrite(p_quartic))
        # TODO show galois wagging his finger or something

        # TODO video of ti 84
        pass

class SearchIntervals(Scene):
    pass


class Temp(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-5, 5, 1],
            # to avoid this, you can probably do masking with Intersection
            x_length=FullScreenRectangle().width,
            y_length=FullScreenRectangle().height,
            x_axis_config={
                "numbers_with_elongated_ticks": np.arange(-10, 10, 5),
            },
            tips=False,
        )
        
        axes_labels = axes.get_axis_labels()
        p_fun = lambda x: .2 * (x - 2) * (x - 9)
        p_graph = axes.plot(p_fun, color=BLUE)

        plot = VGroup(axes, p_graph)
        labels = VGroup(axes_labels)
        interval_start = 0.5
        interval_end = 5
        start_line = axes.get_vertical_line(axes.coords_to_point(interval_start, p_fun(interval_start)))
        end_line = axes.get_vertical_line(axes.coords_to_point(interval_end, p_fun(interval_end)))
        self.play(Create(plot), Create(labels), Create(start_line), Create(end_line))

        # add random dots
        dots = []
        for i in range(10):
            x = random.random() * (interval_end - interval_start) + interval_start
            y = p_fun(x)
            point = axes.coords_to_point(x, y)
            dot = Dot(point, color=YELLOW, fill_opacity=0.5)
            dots.append(dot)
            self.add(dot)
            self.wait(0.1)
        self.play(Uncreate(dot) for dot in dots)

        # steps
        x = interval_start
        x_step = 0.42
        dots = []
        while True:
            point = axes.coords_to_point(x, p_fun(x))
            dot = Dot(point, color=YELLOW, fill_opacity=0.5)
            dots.append(dot)
            self.play(Create(dot))
            if not (p_fun(x) >= 0):
                # want it to run one extra time
                break
            x += x_step
        
        # zoom in to new interval using moving scene
        
        return
