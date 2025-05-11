import os
import sys
from manim import *

script_dir = os.path.dirname(os.path.realpath(__file__))
def local_path(path: str) -> str:
    return os.path.join(script_dir, path)

monospace = "Monospace"
if sys.platform == 'win32':
    monospace = 'consolas'
elif sys.platform == 'darwin':
    monospace = 'monaco'

class Grammar(Scene):
    def construct(self):
        pass


class ExpressionGrammar(Scene):
    def construct(self):
        expression_grammar = MathTex(
            r"e ::=~& n && \text{(number)} \\",
            r"\mid~& \text{true} && \text{(boolean literal)} \\",
            r"\mid~& \text{false} && \text{(boolean literal)} \\",
            r"\mid~& x && \text{(variable)} \\",
            r"\mid~& \text{let}~x = e_1~\text{in}~e_2 && \text{(local variable definition)} \\",
            r"\mid~& e_1 + e_2 && \text{(addition)} \\",
            r"\mid~& e_1 \mid\mid e_2 && \text{(or)} \\",
            r"\mid~& e_1 == e_2 && \text{(equality check)} \\",
            r"\mid~& \text{FUN}~(x : \tau) \rightarrow e && \text{(anonymous function)} \\",
            r"\mid~& e_1(e_2) && \text{(application)} \\",
            r"\mid~& \text{letfun}~f (x : \tau) \rightarrow e_1~\text{in}~e_2 && \text{(recursive function definition)}",
        )
        expression_grammar.scale(0.9)
        self.add(expression_grammar)


class TypeGrammar(Scene):
    def construct(self):
        type_grammar = MathTex(
            r"\tau ::=~& \text{Number} && \text{(number type)} \\",
            r"\mid~& \text{Boolean} && \text{(boolean type)} \\",
            r"\mid~& \tau_{\text{arg}} \rightarrow \tau_{\text{ret}} && \text{(function type)} \\",
        )
        self.add(type_grammar)

numRule = MathTex(
    r"\frac{}{\Gamma \vdash n : \text{Number}}(\text{NUM})"
)
trueRule = MathTex(
    r"\frac{}{\Gamma \vdash \text{true} : \text{Boolean}}(\text{TRUE})"
)
falseRule = MathTex(
    r"\frac{}{\Gamma \vdash \text{false} : \text{Boolean}}(\text{FALSE})"
)
letRule = MathTex(
    r"\frac{\Gamma \vdash e_1 : \tau_1 \qquad \Gamma,x:\tau_1 \vdash e_2 : \tau_2}{\Gamma \vdash \text{let}~x = e_1~\text{in}~e_2 : \tau_2}(\text{LET})"
)
varRule = MathTex(
    r"\frac{\Gamma [x] = \tau}{\Gamma \vdash x : \tau}(\text{VAR})"
)
plusRule = MathTex(
    r"\frac{\Gamma \vdash e_1 : \text{Number} \qquad \Gamma \vdash e_2 : \text{Number}}{\Gamma \vdash e_1 + e_2 : \text{Number}}(\text{PLUS})"
)
orRule = MathTex(
    r"\frac{\Gamma \vdash e_1 : \text{Boolean} \qquad \Gamma \vdash e_2 : \text{Boolean}}{\Gamma \vdash e_1 \mid\mid e_2 : \text{Boolean}}(\text{OR})"
)
equalRule = MathTex(
    r"\frac{\Gamma \vdash e_1 : \tau \qquad \Gamma \vdash e_2 : \tau}{\Gamma \vdash e_1 == e_2 : \text{Boolean}}(\text{EQ})"
)
funRule = MathTex(
    r"\frac{\Gamma,x:\tau_x \vdash e : \tau_e}{\Gamma \vdash \text{fun}~(x : \tau_x) \rightarrow e : \tau_x \rightarrow \tau_e}(\text{FUN})"
)
callRule = MathTex(
    r"\frac{\Gamma \vdash e_1 : \tau_{\text{arg}} \rightarrow \tau_{\text{ret}} \qquad \Gamma \vdash e_2 : \tau_{\text{arg}}}{\Gamma \vdash e_1(e_2) : \tau_{\text{ret}}}(\text{CALL})"
)
letFunRule = MathTex(
    r"\frac{\Gamma,f:\tau_x \rightarrow \tau_1,x:\tau_x \vdash e_1 : \tau_1 \qquad \Gamma,f:\tau_x \rightarrow \tau_1 \vdash e_2 : \tau_2}{\Gamma \vdash \text{letfun}~f (x : \tau_x) \rightarrow e_1~\text{in}~e_2 : \tau_2}(\text{LETFUN})"
).scale(0.8)


letCheckExample = MathTex(
    r"""
    \cfrac{\displaystyle
      \cfrac{}{\displaystyle \cdot \vdash 1 : \text{Number}}(\text{NUM})
      \qquad
      \cfrac{}{\displaystyle x:\text{Number} \vdash x : \text{Number}}(\text{VAR})
    }{\displaystyle
      \cdot \vdash \text{let}~x = 1~\text{in}~x : \text{Number}
    }(\text{LET})
    """
)
letCheckExample.scale(0.8)

class Test(Scene):
    def construct(self):
        self.add(letCheckExample)

class Intro(Scene):
    def construct(self):
        expression_grammar = MathTex(
            r"e ::=~& n && \text{(number)} \\",
            r"\mid~& \text{true} && \text{(boolean literal)} \\",
            r"\mid~& \text{false} && \text{(boolean literal)} \\",
            r"\mid~& x && \text{(variable)} \\",
            r"\mid~& \text{let}~x = e_1~\text{in}~e_2 && \text{(local variable definition)} \\",
            r"\mid~& e_1 + e_2 && \text{(addition)} \\",
            r"\mid~& e_1 \mid\mid e_2 && \text{(or)} \\",
            r"\mid~& e_1 == e_2 && \text{(equality check)} \\",
            r"\mid~& \text{if}~e_1~\text{then}~e_2~\text{else}~e_3 && \text{(conditional)} \\",
            r"\mid~& \text{FUN}~(x : \tau) \rightarrow e && \text{(anonymous function)} \\",
            r"\mid~& e_1(e_2) && \text{(application)} \\",
            r"\mid~& \text{letfun}~f (x : \tau) \rightarrow e_1~\text{in}~e_2 && \text{(recursive function definition)}",
        )
        expression_grammar.scale(0.8)
        self.play(Write(expression_grammar))
        self.wait()
        self.play(Unwrite(expression_grammar))
        self.wait()

        let_example = MathTex(r"\text{let}~x = 1~\text{in}~x + x")
        self.play(Write(let_example))
        self.wait()
        let_result = MathTex(r"2").next_to(let_example, direction=DOWN)
        self.play(Write(let_result))
        self.play(Unwrite(let_example), Unwrite(let_result))
        self.wait()

        if_example = MathTex(r"\text{if}~1 == 2~\text{then}~100~\text{else}~42")
        self.play(Write(if_example))
        self.wait()
        if_result = MathTex(r"42").next_to(if_example, direction=DOWN)
        self.play(Write(if_result))
        self.wait()
        self.play(Unwrite(if_example), Unwrite(if_result))
        self.wait()

        fun_example = MathTex(r"(x : \text{Number}) \to x + 1")
        self.play(Write(fun_example))
        self.wait()
        self.play(Unwrite(fun_example))
        self.wait()

        example = MathTex(r"\text{let}~add1 = {{(x : \text{Number}) \to x + 1}}~\text{in}~add1{{(3)}}")
        result = MathTex(r"4").next_to(example, direction=DOWN)
        self.play(Write(example))
        self.wait()
        self.play(Write(result))
        self.wait()

        example2 = MathTex(r"({{(x : \text{Number}) \to x + 1}}){{(3)}}")
        self.play(Transform(example, example2))
        self.wait()
        self.play(Unwrite(example2), Unwrite(example), Unwrite(result))
        self.wait()

        example = MathTex(
            r"~&\text{letfun}~sumTo10 (x : \text{Number}): \text{Number} \to \\", 
            r"~& \qquad \text{if}~x == 10~\text{then}~x~else~x + sumTo10(x + 1) \\",
            r"~&\text{in}~sumTo10(8)"
        )
        result = MathTex(r"27").next_to(example, direction=DOWN)
        self.play(Write(example))
        self.wait()
        self.play(Write(result))
        self.wait()
        self.play(Unwrite(example), Unwrite(result))
        self.wait()

        type_grammar = MathTex(
            r"\tau ::=~& \text{Number} && \text{(number type)} \\",
            r"\mid~& \text{Boolean} && \text{(boolean type)} \\",
            r"\mid~& \tau_{\text{arg}} \rightarrow \tau_{\text{ret}} && \text{(function type)} \\",
        )
        self.play(Write(type_grammar))
        self.wait()
        self.play(Unwrite(type_grammar))
        self.wait()

class Rules(Scene):
    def construct(self):
        title = Text("Typing Rules", font_size=64)
        self.play(Write(title))
        self.wait()
        self.play(Unwrite(title))

        infer = MathTex(r"\text{infer}: \text{Expression} \to \text{Type}")
        check = MathTex(r"\text{check}: \text{Expression}, \text{Type} \to \text{Void}").next_to(infer, direction=DOWN*2)
        VGroup(infer, check).center()
        self.play(Write(infer))
        self.wait()
        self.play(Write(check))
        self.wait()
        self.play(Unwrite(infer), Unwrite(check))

        java_example = Code(code="int x = 1; return x + x", language="java")
        let_example = MathTex(r"\text{let}~x = 1~\text{in}~x + x").next_to(java_example, direction=DOWN*2)
        VGroup(java_example, let_example).center()

        self.play(Write(java_example))
        self.wait()
        self.play(Write(let_example))
        self.wait()
        self.play(FadeOut(java_example), Unwrite(let_example))

        numRule = MathTex(
            r"\frac{}{ \Gamma \vdash n : \text{Number}}(\text{NUM})",
        )

        self.play(Write(numRule))
        self.wait()
        self.play(Circumscribe(numRule[0][1]))
        self.wait()
        self.play(Circumscribe(numRule[0][3]))
        self.wait()
        self.play(Circumscribe(numRule[0][5:11]))
        self.wait()
        self.play(Circumscribe(numRule[0][12:15]))
        self.wait()
        labels = index_labels(numRule[0])
        # self.add(labels)
        self.play(Unwrite(numRule))
        # self.remove(labels)
        self.wait()
        
        true_rule = MathTex(
            r"\frac{}{\Gamma \vdash \text{true} : \text{Boolean}}(\text{TRUE})"
        )
        false_rule = MathTex(
            r"\frac{}{\Gamma \vdash \text{false} : \text{Boolean}}(\text{FALSE})"
        )
        group = VGroup(true_rule, false_rule).arrange(DOWN, 2).center()
        self.play(Write(group))
        self.wait()
        self.play(Unwrite(group))
        self.wait()


        let_rule = MathTex(
            r"\frac{\Gamma \vdash e_1 : \tau_1 \qquad \Gamma,x:\tau_1 \vdash e_2 : \tau_2}{\Gamma \vdash \text{let}~x = e_1~\text{in}~e_2 : \tau_2}(\text{LET})"
        )
        labels = index_labels(let_rule[0])
        self.play(Write(let_rule))
        self.wait()
        self.play(Circumscribe(let_rule[0][0:7]), Circumscribe(let_rule[0][7:19]))
        self.wait()
        self.play(Circumscribe(let_rule[0][2:7]))
        self.wait()
        self.play(Circumscribe(let_rule[0][9:13]))
        self.wait()
        self.play(Circumscribe(let_rule[0][14:18]))
        self.wait()
        arrow = Arrow(start=let_rule[0][17], end=let_rule[0][34], color=YELLOW, buff=0.1)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(Unwrite(arrow))
        self.wait()
        # self.add(labels)
        self.wait()
        self.play(Unwrite(let_rule))
        # self.remove(labels)
        self.wait()

        var_rule = MathTex(
            r"\frac{\Gamma [x] = \tau}{\Gamma \vdash x : \tau}(\text{VAR})"
        )
        self.play(Write(var_rule))
        self.wait()
        self.play(Unwrite(var_rule))
        self.wait()

        mobs = [
            MathTex(r"{{\cdot \vdash \text{let}~x = 1~\text{in}~x : \text{?}}}"),
            MathTex(r"""
            \cfrac{\displaystyle
            \cdot \vdash 1 : \text{?} \qquad \displaystyle x:\text{?} \vdash x : \text{?}
            }{\displaystyle
            {{\cdot \vdash \text{let}~x = 1~\text{in}~x : \text{?}}} }(\text{LET})
            """),
            MathTex(r"""
            \cfrac{\displaystyle
            \cfrac{}{\displaystyle \cdot \vdash 1 : \text{Number}}(\text{NUM})
            \qquad
            \displaystyle x:\text{?} \vdash x : \text{?}
            }{\displaystyle
            {{\cdot \vdash \text{let}~x = 1~\text{in}~x : \text{?}}} }(\text{LET})
            """),
            MathTex(r"""
            \cfrac{\displaystyle
            \cfrac{}{\displaystyle \cdot \vdash 1 : \text{Number}}(\text{NUM})
            \qquad
            \displaystyle x:\text{Number} \vdash x : \text{?}
            }{\displaystyle
            {{\cdot \vdash \text{let}~x = 1~\text{in}~x : \text{?}}} }(\text{LET})
            """),
            MathTex(
            r"""
            \cfrac{\displaystyle
            \cfrac{}{\displaystyle \cdot \vdash 1 : \text{Number}}(\text{NUM})
            \qquad
            \cfrac{}{\displaystyle x:\text{Number} \vdash x : \text{Number}}(\text{VAR})
            }{\displaystyle
            {{\cdot \vdash \text{let}~x = 1~\text{in}~x : \text{?}}} }
            }(\text{LET})
            """).scale(0.8),
            MathTex(
            r"""
            \cfrac{\displaystyle
            \cfrac{}{\displaystyle \cdot \vdash 1 : \text{Number}}(\text{NUM})
            \qquad
            \cfrac{}{\displaystyle x:\text{Number} \vdash x : \text{Number}}(\text{VAR})
            }{\displaystyle
            \cdot \vdash \text{let}~x = 1~\text{in}~x : {{\text{?}}} }
            }(\text{LET})
            """).scale(0.8),
            MathTex(
            r"""
            \cfrac{\displaystyle
            \cfrac{}{\displaystyle \cdot \vdash 1 : \text{Number}}(\text{NUM})
            \qquad
            \cfrac{}{\displaystyle x:\text{Number} \vdash x : \text{Number}}(\text{VAR})
            }{\displaystyle
            \cdot \vdash \text{let}~x = 1~\text{in}~x : {{\text{Number}}} }
            }(\text{LET})
            """).scale(0.8),
        ]
        self.play(Write(mobs[0]))
        self.wait()
        self.play(TransformMatchingTex(mobs[0], mobs[1]))
        self.wait()
        self.play(ReplacementTransform(mobs[1], mobs[2]))
        self.wait()
        self.play(ReplacementTransform(mobs[2], mobs[3]))
        self.wait()
        self.play(TransformMatchingTex(mobs[3], mobs[4])) # TODO clean this up, it just fades
        self.wait()
        self.remove(mobs[4])
        self.add(mobs[5])
        self.play(TransformMatchingTex(mobs[5], mobs[6]))
        self.wait()
        self.play(Unwrite(mobs[6]))
        self.wait()


        plus_rule = MathTex(
            r"\frac{\Gamma \vdash e_1 : \text{Number} \qquad \Gamma \vdash e_2 : \text{Number}}{\Gamma \vdash e_1 + e_2 : \text{Number}}(\text{PLUS})"
        )
        or_rule = MathTex(
            r"\frac{\Gamma \vdash e_1 : \text{Boolean} \qquad \Gamma \vdash e_2 : \text{Boolean}}{\Gamma \vdash e_1 \mid\mid e_2 : \text{Boolean}}(\text{OR})"
        )
        group = VGroup(plus_rule, or_rule).arrange(direction=DOWN, buff=2).center()
        self.play(Write(group))
        self.wait()
        self.play(Unwrite(group))
        self.wait()

        equal_rule = MathTex(
            r"\frac{\Gamma \vdash e_1 : \tau \qquad \Gamma \vdash e_2 : \tau}{\Gamma \vdash e_1 == e_2 : \text{Boolean}}(\text{EQ})"
        )
        self.play(Write(equal_rule))
        self.wait()
        self.play(Unwrite(equal_rule))
        self.wait()

        if_rule = MathTex(
            r"\frac{\Gamma \vdash e_1 : \text{Boolean} \qquad \Gamma \vdash e_2 : \tau \qquad \Gamma \vdash e_3 : \tau}{\Gamma \vdash \text{if}~e_1~\text{then}~e_2~\text{else}~e_3 : \tau}(\text{IF})"
        )
        self.play(Write(if_rule))
        self.wait()
        self.play(Unwrite(if_rule))
        self.wait()

        fun_rule = MathTex(
            r"\frac{\Gamma,x:\tau_x \vdash e : \tau_e}{\Gamma \vdash \text{fun}~(x : \tau_x) \rightarrow e : \tau_x \rightarrow \tau_e}(\text{FUN})"
        )
        labels = index_labels(fun_rule[0])
        self.play(Write(fun_rule))
        self.wait()
        self.play(Circumscribe(fun_rule[0][18:22]), Circumscribe(fun_rule[0][26:28]))
        self.wait()
        self.play(Circumscribe(fun_rule[0][9:11]), Circumscribe(fun_rule[0][29:31]))
        # self.add(labels)
        self.wait()
        self.play(Unwrite(fun_rule))
        # self.remove(labels)

        example = MathTex(r"{{\text{fun}~(x) \to {{x + 1}}}}")
        labels = index_labels(example[0])
        example_annotated = MathTex(r"{{\text{fun}~(x) \to {{x + 1}}}} : \text{Number} \to \text{Number}")
        self.play(Write(example))
        # self.add(labels)
        self.wait()
        self.play(Circumscribe(example[0][7:10]))
        self.wait()
        self.play(TransformMatchingTex(example, example_annotated))
        self.wait()
        self.play(Unwrite(example_annotated))
        self.wait()

        call_rule = MathTex(
            r"\frac{\Gamma \vdash e_1 : \tau_{\text{arg}} \rightarrow \tau_{\text{ret}} \qquad \Gamma \vdash e_2 : \tau_{\text{arg}}}{\Gamma \vdash e_1(e_2) : \tau_{\text{ret}}}(\text{CALL})"
        )
        labels = index_labels(call_rule[0])
        self.play(Write(call_rule))
        self.wait()
        self.play(*[Circumscribe(call_rule[0][a:b]) for a,b in [[26,28],[2,14]]])
        self.wait()
        self.play(*[Circumscribe(call_rule[0][a:b]) for a,b in [[5,9],[29,31],[16,23]]])
        self.wait()
        self.play(*[Circumscribe(call_rule[0][a:b]) for a,b in [[10,14],[33,37]]])
        self.wait()
        # self.add(labels)
        self.play(Unwrite(call_rule))
        self.wait()

        def Emphasize(mob):
            # return Indicate(let_fun_rule[0][a:b], scale_factor=1.05, run_time=1)
            return Circumscribe(mob, time_width=8, run_time=3)

        let_fun_rule = MathTex(
            r"\frac{\Gamma,f:\tau_x \rightarrow \tau_{\text{ret}},x:\tau_x \vdash e_1 : \tau_{\text{ret}} \qquad \Gamma,f:\tau_x \rightarrow \tau_{\text{ret}} \vdash e_2 : \tau_2}{\Gamma \vdash \text{letfun}~f (x : \tau_x) : \tau_{\text{ret}} \rightarrow e_1~\text{in}~e_2 : \tau_2}(\text{LETFUN})"
        ).scale(0.8)
        labels = index_labels(let_fun_rule[0]).shift(DOWN*0.2)
        self.play(Write(let_fun_rule))
        self.wait()
        self.play(*[Emphasize(let_fun_rule[0][a:b]) for a,b in [[17,24],[25,41],[65,72]]])
        self.wait()
        self.play(*[Emphasize(let_fun_rule[0][a:b]) for a,b in [[51,57],[62,65],[11,24]]])
        self.wait()
        self.play(*[Emphasize(let_fun_rule[0][a:b]) for a,b in [[2,11],[17,19],[50,51],[63,65]]])
        self.wait()
        self.play(*[Emphasize(let_fun_rule[0][a:b]) for a,b in [[57,62]]])
        self.wait()
        arrow = Arrow(start=let_fun_rule[0][58], end=let_fun_rule[0][10], buff=0.1, color=YELLOW)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrow))
        self.add(labels)
        self.play(Unwrite(let_fun_rule))
        self.wait()

