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
)
letFunRule.scale(0.8)


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
            r"\mid~& \text{FUN}~(x : \tau) \rightarrow e && \text{(anonymous function)} \\",
            r"\mid~& e_1(e_2) && \text{(application)} \\",
            r"\mid~& \text{letfun}~f (x : \tau) \rightarrow e_1~\text{in}~e_2 && \text{(recursive function definition)}",
        )
        expression_grammar.scale(0.9)
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
        mob = Tex(
            r"\begin{itemize}\item{foo}\end{itemize}",
        )
        self.add(mob)




