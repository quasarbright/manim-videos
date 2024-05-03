from manim import *

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

        numbers = VGroup(MathTex('1'), MathTex('-12'), MathTex('3.14')).arrange(DOWN, buff=2)
        booleans = VGroup(MathTex('\mathrm{true}'), MathTex('\mathrm{false}')).arrange(DOWN, buff=2)
        constants = VGroup(numbers, booleans).arrange(RIGHT, buff=2)
        self.play(Write(constants))
        self.wait(1)
        self.play(Unwrite(constants))

        formulas = [
            MathTex('{{2 + 2}}'),
            MathTex('\mathrm{eval}( {{2 + 2}} )'),
            MathTex('4'),
        ]

        diagram = VGroup(
            Tex('expressions'),
            VGroup(
                MathTex('\mathrm{eval}'),
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

        two = MathTex('{{2}}')
        self.play(Write(two))
        self.wait(1)
        formulas = [
            two,
            MathTex('\mathrm{eval}( {{2}} )'),
            MathTex('{{2}}'),
        ]
        for a,b in zip(formulas,formulas[1::]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)
        self.play(Unwrite(formulas[-1]))

        formulas = [
            MathTex('{{true}}'),
            MathTex('\mathrm{eval}( {{true}} )'),
            MathTex('{{true}}'),
        ]
        self.play(Write(formulas[0]))
        for a,b in zip(formulas,formulas[1::]):
            self.play(TransformMatchingTex(a,b))
        self.wait(1)
        sunglasses = ImageMobject("images/sunglasses.png").scale(1).next_to(formulas[-1], DOWN * 2)
        self.play(FadeIn(sunglasses))
        self.wait(1)
        self.play(Unwrite(formulas[-1]), FadeOut(sunglasses))

class Operations(Scene):
    def construct(self):
        title = Text('Operations', font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(Unwrite(title))

        ops = VGroup(
            MathTex('+'),
            MathTex('-'),
            MathTex('*'),
            MathTex('/'),
        ).arrange(RIGHT, buff=2)
        self.play(Write(ops))
        self.wait(1)
        self.play(Unwrite(ops))

        addition = MathTex('1 + 1')
        self.play(Write(addition))
        self.wait(1)
        self.play(Unwrite(addition))

        formulas = [
            MathTex('{{E_1}} + {{E_2}}'),
            MathTex('{{HUGE_1}} + {{HUGE_2}}'),
            MathTex('{{E_1}} + {{E_2}}'),
            MathTex('\mathrm{eval}( {{E_1}} {{+}} {{E_2}} )'),
            MathTex('\mathrm{eval}( {{E_1}} ) {{+}} \mathrm{eval}( {{E_2}} )'),
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

        code = Text('eval(e1) + eval(e2)', font="consolas")
        self.play(Write(code))
        self.wait(1)
        self.play(Unwrite(code))

        turtles = ImageMobject('images/turtles.png').scale(0.5)
        self.play(FadeIn(turtles))
        self.wait(1)
        self.play(FadeOut(turtles))

        formula = MathTex(r'\text{eval}', '(', 'E_1', ')', '+', r'\text{eval}', '(', 'E_2', ')')
        formula_yellow = formula.copy()
        for tex in [r'\text{eval}', '+', '(', ')']:
            formula_yellow.set_color_by_tex(tex, YELLOW)
        self.play(Write(formula))
        self.wait(1)
        self.play(FadeIn(formula_yellow))
        self.remove(formula)
        self.wait(1)
