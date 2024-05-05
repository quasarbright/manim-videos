from typing import Union
import os
from manim import *
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
def local_path(path: str) -> str:
    return os.path.join(script_dir, path)

monospace = "Monospace"
if sys.platform == 'win32':
    monospace = 'consolas'
elif sys.platform == 'darwin':
    monospace = 'monaco'

def make_color_map(strings, color):
    return {string: color for string in strings}

def eval_colors(mob: MathTex, strings):
    return mob.set_color(YELLOW).set_color_by_tex_to_color_map(make_color_map(strings, WHITE))

def EvalTex(*texs: str | List[str]):
    return eval_colors(
        MathTex(*[
            tex if isinstance(tex, str) else r'\mathtt{' + tex[0] + '}'
            for tex in texs
        ]),
        [r'\mathtt{' + tex[0] + '}' for tex in texs if isinstance(tex, list)]
    )


class Title(Scene):
    def construct(self):
        title = Text("How to Make an Interpreter", 42)
        self.play(Write(title))
        self.wait(1)
        self.play(Unwrite(title))
        self.wait(1)

class Intro(Scene):
    def construct(self):

        factorial = VGroup(
            MathTex(r'\mathrm{letrec}\ factorial = \mathrm{function}\ (n) \Rightarrow'),
            indented := VGroup(
                MathTex(r'\mathrm{if}\ n == 0'),
                MathTex(r'\mathrm{then}\ 1'),
                MathTex(r'\mathrm{else}\ n * factorial(n - 1)'),
            ).arrange(DOWN, aligned_edge=LEFT),
            MathTex(r'\mathrm{in}'),
            MathTex(r'factorial(4)'),
        ).arrange(DOWN, aligned_edge=LEFT)
        indented.shift(RIGHT)
        factorial = Tex(r'''
                        \begin{verbatim}
                        letrec factorial = function (n) =>
                          if n == 0
                          then 1
                          else n * factorial(n - 1)
                        in
                        factorial(4)
                        \end{verbatim}
                        ''')
        self.play(Write(factorial))
        self.wait(1)
        self.play(Unwrite(factorial))
        self.wait(1)

class Constants(Scene):
    def construct(self):
        title = Text("Constants", 42)
        self.play(Write(title))
        self.wait(1)
        self.play(Unwrite(title))

        numbers = VGroup(MathTex(r'\mathtt{1}'), MathTex(r'\mathtt{-12}'), MathTex(r'\mathtt{3.14}')).arrange(DOWN, buff=2)
        booleans = VGroup(MathTex(r'\mathtt{true}'), MathTex(r'\mathtt{false}')).arrange(DOWN, buff=2)
        constants = VGroup(numbers, booleans).arrange(RIGHT, buff=2)
        self.play(Write(constants))
        self.wait(1)
        self.play(Unwrite(constants))

        formulas = [
            MathTex(r'{{\mathtt{2 + 2}}}'),
            MathTex(r'\mathrm{eval}( {{\mathtt{2 + 2}}})'),
            MathTex(r'\mathtt{4}'),
        ]

        diagram = VGroup(
            Tex('expressions'),
            VGroup(
                MathTex(r'\mathrm{eval}'),
                Arrow(ORIGIN, RIGHT*3),
            ).arrange(DOWN),
            Tex('values')
        ).arrange(RIGHT, aligned_edge=DOWN).next_to(formulas[1], DOWN * 2)

        self.play(Write(formulas[0]))

        self.play(TransformMatchingTex(formulas[0], formulas[1]), Create(diagram))
        self.wait(1)
        self.play(TransformMatchingTex(formulas[1], formulas[2]))
        self.wait(1)
        self.play(Unwrite(formulas[-1]), Uncreate(diagram))

        two = MathTex(r'{{\mathtt{2}}}')
        self.play(Write(two))
        self.wait(1)
        formulas = [
            two,
            MathTex(r'\mathrm{eval}( {{\mathtt{2}}} )'),
            MathTex(r'{{\mathtt{2}}}'),
        ]
        for a,b in zip(formulas,formulas[1::]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)
        self.play(Unwrite(formulas[-1]))

        formulas = [
            MathTex(r'{{\mathtt{true}}}'),
            MathTex(r'\mathrm{eval}( {{\mathtt{true}}} )'),
            MathTex(r'{{\mathtt{true}}}'),
        ]
        self.play(Write(formulas[0]))
        for a,b in zip(formulas,formulas[1::]):
            self.play(TransformMatchingTex(a,b))
        self.wait(1)
        sunglasses = ImageMobject(local_path("images/sunglasses.png")).scale(1).next_to(formulas[-1], DOWN * 2)
        self.play(FadeIn(sunglasses))
        self.wait(1)
        self.play(Unwrite(formulas[-1]), FadeOut(sunglasses))
        self.wait(1)

class Operations(Scene):
    def construct(self):
        title = Text('Operations', font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(Unwrite(title))

        ops = VGroup(
            MathTex(r'\mathtt{+}'),
            MathTex(r'\mathtt{-}'),
            MathTex(r'\mathtt{*}'),
            MathTex(r'\mathtt{/}'),
        ).arrange(RIGHT, buff=2)
        self.play(Write(ops))
        self.wait(1)
        self.play(Unwrite(ops))

        addition = MathTex(r'\mathtt{1 + 1}')
        self.play(Write(addition))
        self.wait(1)
        self.play(Unwrite(addition))

        formulas = [
            MathTex(r'{{\mathtt{E_1}}} + {{\mathtt{E_2}}}'),
            MathTex(r'{{\mathtt{HUGE_1}}} + {{\mathtt{HUGE_2}}}'),
            MathTex(r'{{\mathtt{E_1}}} + {{\mathtt{E_2}}}'),
            MathTex(r'\mathrm{eval}( {{\mathtt{E_1}}} {{\mathtt{+}}} {{\mathtt{E_2}}} )'),
            MathTex(r'\mathrm{eval}( {{\mathtt{E_1}}} ) {{+}} \mathrm{eval}( {{\mathtt{E_2}}} )'),
        ]
        self.play(Write(formulas[0]))
        for a,b in zip(formulas, formulas[1::]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)

        alert = Text('!', font_size=600, color=PURE_RED)
        self.add(alert)
        self.wait(1)
        self.play(FadeOut(alert))
        self.wait(1)
        self.play(formulas[-1].animate.set_color_by_tex('+', RED))
        self.wait(1)
        self.play(Unwrite(formulas[-1]))

        code = Text('eval(E1) + eval(E2)', font=monospace)
        self.play(Write(code))
        self.wait(1)
        self.play(Unwrite(code))

        turtles = ImageMobject(local_path('images/turtles.png')).scale(0.5)
        self.play(FadeIn(turtles))
        self.wait(1)
        self.play(FadeOut(turtles))

        formula = MathTex(r'\text{eval}', '(', r'\mathtt{E_1}', ')', '+', r'\text{eval}', '(', r'\mathtt{E_2}', ')')
        formula_yellow = formula.copy()
        for tex in [r'\text{eval}', '+', '(', ')']:
            formula_yellow.set_color_by_tex(tex, YELLOW)
        self.play(Write(formula))
        self.wait(1)
        self.play(FadeIn(formula_yellow))
        self.wait(1)
        self.remove(formula)
        self.play(Unwrite(formula_yellow))
        self.wait(1)

        formulas = [
            MathTex(r'\mathtt{1 + {{true}}}'),
            MathTex(r'\mathtt{1 + {{1}}}'),
            MathTex(r'\mathtt{1 + {{true}}}'),
        ]
        self.play(Write(formulas[0]))
        self.wait(1)
        for a,b in zip(formulas, formulas[1::]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)
        self.play(formulas[-1].animate.set_color(RED), Wiggle(formulas[-1]))
        self.wait(1)
        self.play(formulas[-1].animate.set_color(WHITE))
        self.wait(1)
        self.play(Unwrite(formulas[-1]))
        self.wait(1)

        formulas = [
            MathTex(r'\mathrm{eval}(', r'\mathtt{2 * 3}', r'\mathtt{+}', r'\mathtt{10 / 5}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{2 * 3}': WHITE, r'\mathtt{+}': WHITE, r'\mathtt{10 / 5}': WHITE
            }),
            MathTex(r'\mathrm{eval}(', r'\mathtt{2 * 3}', ')', '+', r'\mathrm{eval}(', r'\mathtt{10 / 5}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{2 * 3}': WHITE, r'\mathtt{10 / 5}': WHITE
            }),
            MathTex('(', r'\mathrm{eval}(', r'\mathtt{2}', r')', '*', r'\mathrm{eval}(', r'\mathtt{3}', ')', ')', '+', r'\mathrm{eval}(', r'\mathtt{10 / 5}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{2}': WHITE, r'\mathtt{3}': WHITE, r'\mathtt{10 / 5}': WHITE
            }),
            MathTex('(', r'\mathtt{2}', '*', r'\mathrm{eval}(', r'\mathtt{3}', ')', ')', '+', r'\mathrm{eval}(', r'\mathtt{10 / 5}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{3}': WHITE, r'\mathtt{10 / 5}': WHITE
            }),
            MathTex('(', r'\mathtt{2}', '*', r'\mathtt{3}', ')', '+', r'\mathrm{eval}(', r'\mathtt{10 / 5}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{10 / 5}': WHITE
            }),
            MathTex(r'\mathtt{6}', '+', r'\mathrm{eval}(', r'\mathtt{10 / 5}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{10 / 5}': WHITE
            }),
            MathTex(r'\mathtt{6}', '+', '(', r'\mathrm{eval}(', r'\mathtt{10}', ')', '/', r'\mathrm{eval}(', r'\mathtt{5}', ')', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{10}': WHITE, r'\mathtt{5}': WHITE,
            }),
            MathTex(r'\mathtt{6}', '+', '(', r'\mathtt{10}', '/', r'\mathrm{eval}(', r'\mathtt{5}', ')', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{5}': WHITE,
            }),
            MathTex(r'\mathtt{6}', '+', '(', r'\mathtt{10}', '/', r'\mathtt{5}', ')').set_color(YELLOW),
            MathTex(r'\mathtt{6}', '+', r'\mathtt{2}').set_color(YELLOW),
            MathTex(r'\mathtt{8}').set_color(YELLOW),
        ]
        self.play(Write(formulas[0]))
        self.wait(1)
        for a,b in zip(formulas, formulas[1::]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)
        self.play(Unwrite(formulas[-1]))

        formulas = [
            MathTex(r'\mathrm{eval}', '(', r'\mathtt{1}', '/', r'\mathtt{0}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{1}': WHITE, '/': WHITE, r'\mathtt{0}': WHITE,
            }),
            MathTex(r'\mathrm{eval}', '(', r'\mathtt{1}', ')', '/', r'\mathrm{eval}', '(', r'\mathtt{0}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{1}': WHITE, r'\mathtt{0}': WHITE,
            }),
            MathTex(r'\mathtt{1}', '/', r'\mathrm{eval}', '(', r'\mathtt{0}', ')').set_color(YELLOW).set_color_by_tex_to_color_map({
                r'\mathtt{0}': WHITE,
            }),
            MathTex(r'\mathtt{1}', '/', r'\mathtt{0}').set_color(YELLOW).set_color_by_tex_to_color_map({
            }),
        ]
        self.play(Write(formulas[0]))
        self.wait(1)
        for a,b in zip(formulas, formulas[1::]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)
        self.play(formulas[-1].animate.set_color(RED), Wiggle(formulas[-1]))
        self.wait(1)
        self.play(Unwrite(formulas[-1]))
        self.wait(1)
    
    # TODO what if instead of doing it all in one line, while you do a sub-expression, you do that on a new line
    # then it'll be like the call stack
    # eval(1 + 2)
    # eval(1) + eval(2)
    # eval(1) + eval(2) \n eval(1)
    # eval(1) + eval(2) \n 1
    # 1 + eval(2)
    # 1 + eval(2) \n eval(2)
    # 1 + eval(2) \n 2
    # 1 + 2
    # 3
    # also will avoid the weird stuff with the evals and parens not moving right

class Testing(Scene):
    # the formula can also be False
    def steps(self, formulass: List[List[MathTex]], wait_time=1, keep_last=False):
        # list of tex strings that are currently on screen
        stack = []
        for formulas in formulass:
            animations = []
            for i, formula in enumerate(formulas):
                # animations to be played at the same time
                if i >= len(stack):
                    # this is a new formula
                    assert formula
                    animations.append(Write(formula.to_edge(UP).shift(DOWN * i)))
                    stack.append(formula)
                elif formula and stack[i].tex_string != formula.tex_string:
                    # this is a transformation of an existing formula
                    animations.append(TransformMatchingTex(stack[i], formula.to_edge(UP).shift(DOWN * i)))
                    stack[i] = formula
            for i in range(len(formulas), len(stack)):
                # formulas to remove
                animations.append(Unwrite(stack[i]))
            stack = stack[:len(formulas)]
            self.play(*animations)
            if wait_time > 0:
                self.wait(wait_time)
        if not keep_last:
            if len(stack) > 0:
                self.play(*[Unwrite(formula) for formula in stack])
                if wait_time > 0:
                    self.wait(wait_time)
        else:
            return stack

    def construct(self):
        [formula] = self.steps([
            [
                EvalTex(r'\mathrm{ eval}', ' (', ['2 * 3 + 10 / 2'], ' )'),
            ],
            [
                EvalTex(r'\mathrm{ eval}', ' (', ['2 * 3'], r' )', '+', r'\mathrm{  eval}', '  (', ['10 / 2'], '  )'),
            ],
            [
                False,
                EvalTex(r'\mathrm{ eval}', ' (', ['2 * 3'], r' )'),
            ],
            [
                False,
                EvalTex(r'\mathrm{ eval}', ' (', ['2'], ' )', '*', r'\mathrm{  eval}', '  (', ['3'], r'  )'),
            ],
            [
                False,
                False,
                EvalTex(r'\mathrm{ eval}', ' (', ['2'], r' )'),
            ],
            [
                False,
                False,
                EvalTex(r'\mathtt{2}'),
            ],
            [
                False,
                EvalTex(r'\mathtt{2}', '*', r'\mathrm{  eval}', '  (', ['3'], r'  )'),
            ],
            [
                False,
                False,
                EvalTex(r'\mathrm{ eval}', '  (', ['3'], r'  )'),
            ],
            [
                False,
                False,
                EvalTex(r'\mathtt{3}'),
            ],
            [
                False,
                EvalTex(r'\mathtt{2}', '*', r'\mathtt{3}'),
            ],
            [
                False,
                EvalTex(r'\mathtt{6}'),
            ],
            [
                EvalTex(r'\mathtt{6}', '+', r'\mathrm{  eval}', '  (', ['10 / 2'], '  )'),
            ],
            [
                False,
                EvalTex(r'\mathrm{  eval}', '  (', ['10 / 2'], '  )'),
            ],
            [
                False,
                EvalTex(r'\mathrm{  eval}', '  (', ['10'], r'  )', '/', r'\mathrm{   eval}', '   (', ['2'], '   )'),
            ],
            [
                False,
                False,
                EvalTex(r'\mathrm{  eval}', '  (', ['10'], r'  )'),
            ],
            [
                False,
                False,
                EvalTex(r'\mathtt{10}'),
            ],
            [
                False,
                EvalTex(r'\mathtt{10}', '/', r'\mathrm{   eval}', '   (', ['2'], '   )'),
            ],
            [
                False,
                EvalTex(r'\mathtt{10}', '/', r'\mathrm{   eval}', '(   ', ['2'], '   )'),
                EvalTex(r'\mathrm{   eval}', '   (', ['2'], '   )'),
            ],
            [
                False,
                EvalTex(r'\mathtt{10}', '/', r'\mathrm{   eval}', '   (', ['2'], '   )'),
                EvalTex(r'\mathtt{2}'),
            ],
            [
                False,
                EvalTex(r'\mathtt{10}', '/', r'\mathtt{2}'),
            ],
            [
                False,
                EvalTex(r'\mathtt{5}'),
            ],
            [
                EvalTex(r'\mathtt{6}', '+', r'\mathtt{5}'),
            ],
            [
                EvalTex(r'\mathtt{11}'),
            ],
            [
                EvalTex(r'\mathrm{eval}', '(', ['2 * 3 + 10 / 2'], ')', '=', r'\mathtt{11}'),
            ],
        ], wait_time=0, keep_last=True)