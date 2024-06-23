from dataclasses import dataclass
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

#### BEGIN STEPS

# this is a little DSL for evaluation animations

def make_color_map(strings, color):
    '''creates a color map mapping all tex strings to color'''
    return {string: color for string in strings}

def eval_colors(mob: MathTex, strings):
    '''colors mob so it's yellow, except given strings are white'''
    return mob.set_color(YELLOW).set_color_by_tex_to_color_map(make_color_map(strings, WHITE))

spaces = 0
@dataclass
class EvalOf:
    '''wraps the source_strs in an eval(...) and adds unique whitespaces to eval and parens.
    '''
    # makes the eval and parentheses unique
    spaces: int
    # source code strings, will become white and wrapped with yellow eval(...)
    source_strs: List[str]
    # tex strings to make white, wrapped with \mathtt{...}
    tts: List[str]
    # all tex strings to be rendered
    texs: List[str]
    def __init__(self, *source_strs: str, spaces_: int = False):
        global spaces
        self.source_strs = source_strs
        self.spaces = spaces_ or (spaces := spaces + 1)
        self.tts = [r'\mathtt{' + tt + '}' for tt in source_strs]
        self.texs = [' '*spaces+r'\mathrm{eval}', ' '*spaces+'(', *[tt for tt in self.tts], ' '*spaces+')']
    
    def unique_copy(self):
        '''copy the tex, but make the number of spaces unique'''
        global spaces
        return EvalOf(*self.source_strs, spaces_=(spaces := spaces + 1))

def EvalTex(*texs: str | EvalOf):
    '''handles coloring
    Ex: EvalTex(EvalOf('2'), '+', EvalOf('3'))
    '''
    # TODO just color submobjects by index instead of doing a color map by substring
    texs_ = []
    tts = []
    for tex in texs:
        if isinstance(tex, EvalOf):
            eval_of = tex
            texs_.extend(eval_of.texs)
            tts.extend(eval_of.tts)
        else:
            texs_.append(tex)
    return eval_colors(
        MathTex(*texs_),
        tts,
    )

@dataclass
class Step:
    '''evaluation step'''
    # displayed vertically, bottom is at the "top of the call stack"
    formulas: List[MathTex]
    # if this is False, instead of transforming, just remove the old and add this.
    # useful when doing a re-structure that doesn't change content, to aid a later
    # transformation
    should_transform: bool = True

class InterpreterScene(Scene):
    # the formula can also be False
    def steps(self, steps: List[Step], wait_time=1, keep_last=False) -> VGroup:
        '''reduction steps'''
        mob = False
        for step in steps:
            mobs = [formula and formula.to_edge(UP).shift(DOWN * i) for i, formula in enumerate(step.formulas)]
            for i, formula in enumerate(mobs):
                if not formula:
                    mobs[i] = mob.submobjects[i]
            new_mob = VGroup(*mobs)
            if mob:
                if step.should_transform:
                    self.play(TransformMatchingTex(mob, new_mob))
                    if wait_time > 0:
                        self.wait(wait_time)
                else:
                    self.remove(mob)
                    self.add(new_mob)
            else:
                self.play(Write(new_mob))
                if wait_time > 0:
                    self.wait(wait_time)
            mob = new_mob
        if not keep_last and len(mob.submobjects) > 0:
            self.play(Unwrite(mob))
        return mob

class Testing(InterpreterScene):
    def construct(self):
        # TODO instead of EvalTex taking in a singleton list, take in a Source object which is a dataclass with 1 string field
        # TODO EvalOf is data and instead of rewriting to re-space, call eval_2.copy()
        # TODO EvalTex flattens EvalOf so you don't have to *
        # TODO try to fix the weirdness of '2 * 3' to '2' '*' '3' by having it separated from the beginning
        # You should probably just have These things subclass MathTex or VGroup
        self.steps([
            Step([
                EvalTex(EvalOf('2 * 3', '\ +\ ', '10 / 2')),
            ]),
            Step([
                EvalTex(eval23 := EvalOf('2 * 3'), '+', eval_102 := EvalOf('10 / 2')),
            ]),
            Step([
                False,
                EvalTex(eval23),
            ]),
            Step([
                False,
                # not sure why, but unique_copy doesn't work here
                EvalTex(EvalOf(' 2 * 3')),
            ], should_transform=False),
            Step([
                False,
                EvalTex(EvalOf('2', '\ *\ ', '3')),
            ]),
            Step([
                False,
                EvalTex((eval_2 := EvalOf('2')), '*', (eval_3 := EvalOf('3')))
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{2}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{2}', '*', eval_3),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_3),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_3.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{3}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{2}', '*', r'\mathtt{3}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{6}'),
            ]),
            Step([
                EvalTex(r'\mathtt{6}', '+', eval_102),
            ]),
            Step([
                False,
                EvalTex(eval_102),
            ]),
            Step([
                False,
                EvalTex(eval_102.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                EvalTex(EvalOf('10', r'\ /\ ', '2')),
            ], should_transform=False),
            Step([
                False,
                EvalTex((eval_10 := EvalOf('10')), '/', (eval_2 := EvalOf('2')))
            ]),
            Step([
                False,
                False,
                EvalTex(eval_10),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_10.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{10}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{10}', '/', eval_2),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2)
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2.unique_copy())
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{2}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{10}', '/', r'\mathtt{2}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{5}'),
            ]),
            Step([
                EvalTex(r'\mathtt{6}', '+', r'\mathtt{5}'),
            ]),
            Step([
                EvalTex(r'\mathtt{11}'),
            ]),
            Step([
                EvalTex(EvalOf('2 * 3 + 10 / 2'), '=', r'\mathtt{11}'),
            ]),
        ], wait_time=0, keep_last=True)

### END STEPS

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

class Operations(InterpreterScene):
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

        mob = self.steps([
            Step([
                EvalTex(EvalOf('2 * 3', '\ +\ ', '10 / 2')),
            ]),
            Step([
                EvalTex(eval23 := EvalOf('2 * 3'), '+', eval_102 := EvalOf('10 / 2')),
            ]),
            Step([
                False,
                EvalTex(eval23),
            ]),
            Step([
                False,
                # not sure why, but unique_copy doesn't work here
                EvalTex(EvalOf(' 2 * 3')),
            ], should_transform=False),
            Step([
                False,
                EvalTex(EvalOf('2', '\ *\ ', '3')),
            ]),
            Step([
                False,
                EvalTex((eval_2 := EvalOf('2')), '*', (eval_3 := EvalOf('3')))
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{2}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{2}', '*', eval_3),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_3),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_3.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{3}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{2}', '*', r'\mathtt{3}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{6}'),
            ]),
            Step([
                EvalTex(r'\mathtt{6}', '+', eval_102),
            ]),
            Step([
                False,
                EvalTex(eval_102),
            ]),
            Step([
                False,
                EvalTex(eval_102.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                EvalTex(EvalOf('10', r'\ /\ ', '2')),
            ], should_transform=False),
            Step([
                False,
                EvalTex((eval_10 := EvalOf('10')), '/', (eval_2 := EvalOf('2')))
            ]),
            Step([
                False,
                False,
                EvalTex(eval_10),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_10.unique_copy()),
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{10}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{10}', '/', eval_2),
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2)
            ]),
            Step([
                False,
                False,
                EvalTex(eval_2.unique_copy())
            ], should_transform=False),
            Step([
                False,
                False,
                EvalTex(r'\mathtt{2}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{10}', '/', r'\mathtt{2}'),
            ]),
            Step([
                False,
                EvalTex(r'\mathtt{5}'),
            ]),
            Step([
                EvalTex(r'\mathtt{6}', '+', r'\mathtt{5}'),
            ]),
            Step([
                EvalTex(r'\mathtt{11}'),
            ]),
            Step([
                EvalTex(EvalOf('2 * 3 + 10 / 2'), '=', r'\mathtt{11}'),
            ]),
        ], wait_time=0, keep_last=True)

        self.play(Unwrite(mob))
        self.wait(1)

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

        # comparison
        ops = VGroup(
            MathTex(r'\mathtt{<}'),
            MathTex(r'\mathtt{>}'),
            MathTex(r'\mathtt{==}'),
            MathTex(r'\mathtt{<=}'),
            MathTex(r'\mathtt{>=}'),
        ).arrange(RIGHT, buff=2)
        self.play(Write(ops))
        self.wait(1)
        self.play(Unwrite(ops))

        # eval(E_1 < E_2) = eval(E_1) < eval(E_2)
        mob = EvalTex(
            EvalOf('E1 < E2'),
            '=',
            EvalOf('E1'),
            '<',
            EvalOf('E2'),
        )
        self.play(Write(mob))
        self.wait(1)
        self.play(Unwrite(mob))

        # logic

        ops = VGroup(
            MathTex(r'\mathtt{ \| }'),
            MathTex(r'\mathtt{ \&\& }'),
        ).arrange(RIGHT, buff=2)
        self.play(Write(ops))
        self.wait(1)
        self.play(Unwrite(ops))

        mob = EvalTex(
            EvalOf(r'E1 \| E2'),
            '=',
            EvalOf('E1'),
            r'\|',
            EvalOf('E2'),
        )
        self.play(Write(mob))
        self.wait(1)
        self.play(Unwrite(mob))

        # short circuit
        formulas = [
            EvalTex(EvalOf('false', r'\|', 'HUGE')),
            EvalTex(r'\mathtt{false}', r'\|', EvalOf('HUGE')),
            EvalTex('\mathtt{false}'),
        ]
        self.play(Write(formulas[0]))
        self.wait(1)
        for a,b in zip(formulas, formulas[1:]):
            self.play(TransformMatchingTex(a,b))
            self.wait(1)
        self.play(Unwrite(formulas[-1]))

        # not and negation
        mob = EvalTex(
            EvalOf('!E1'),
            '=',
            '!',
            EvalOf('E1'),
        )
        self.play(Write(mob))
        self.wait(1)
        self.play(Unwrite(mob))
        self.wait(1)
        mob = EvalTex(
            EvalOf('-E1'),
            '=',
            '-',
            EvalOf('E1'),
        )
        self.play(Write(mob))
        self.wait(1)
        self.play(Unwrite(mob))

class If(InterpreterScene):
    def construct(self):
        title = Text('If', font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(Unwrite(title))

        mob = EvalTex(EvalOf('if', '\ ', 'CND', '\ ', 'then', '\ ', 'THN', '\ ', 'else', '\ ', 'ELS'))
        self.play(Write(mob))
        self.wait(1)
        mob2 = EvalTex(EvalOf('CND'), '=', r'\mathtt{true}').shift(DOWN)
        self.play(Write(mob2))
        self.wait(1)
        mob3 = EvalTex(EvalOf('THN'))
        self.play(FadeOut(mob2), TransformMatchingTex(mob, mob3))
        self.wait(1)
        self.play(Unwrite(mob3))

        mob = EvalTex(EvalOf('if', '\ ', 'CND', '\ ', 'then', '\ ', 'THN', '\ ', 'else', '\ ', 'ELS'))
        self.play(Write(mob))
        self.wait(1)
        mob2 = EvalTex(EvalOf('CND'), '=', r'\mathtt{false}').shift(DOWN)
        self.play(Write(mob2))
        self.wait(1)
        mob3 = EvalTex(EvalOf('ELS'))
        self.play(FadeOut(mob2), TransformMatchingTex(mob, mob3))
        self.wait(1)
        self.play(Unwrite(mob3))

        return

class Let(InterpreterScene):
    def construct(self):
        title = Text('Let', font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(Unwrite(title))
        return

class Temp(InterpreterScene):
    def construct(self):


        return
