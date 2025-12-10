from fractions import Fraction
from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class AlgebraicSimplificationPlugin(BasePlugin):
    def __init__(self, amplitude=10):
        self.amplitude = amplitude

    def get_name(self):
        return "代數式化簡"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b, c, d, e, f, g, h = generate_nums(8, self.amplitude)
            while (0 in [a, b, c, d, e, f, g, h]):
                a, b, c, d, e, f, g, h = generate_nums(8, self.amplitude)

            x1 = "x" if a == 1 else "-x" if a == -1 else f"{a}x"
            y1 = "+y" if b == 1 else "-y" if b == -1 else f"+{b}y" if b > 0 else f"{b}y"
            c1 = f"+{c}" if c > 0 else str(c)
            x2 = "x" if d == 1 else "-x" if d == -1 else f"{d}x"
            y2 = "+y" if e == 1 else "-y" if e == -1 else f"+{e}y" if e > 0 else f"{e}y"
            c2 = f"+{f}" if f > 0 else str(f)
            m = "" if g == 1 else "-" if g == -1 else f"{g}" if g > 0 else str(g)
            n = "+" if h == 1 else "-" if h == -1 else f"+{h}" if h > 0 else str(h)
            question = f"{m}({x1}{y1}{c1}){n}({x2}{y2}{c2})"

            coef_x = g * a + h * d
            coef_y = g * b + h * e
            coef_c = g * c + h * f
            ans_x = "" if coef_x == 0 else "x" if coef_x == 1 else "-x" if coef_x == -1 else f"{coef_x}x" if coef_x > 0 else f"{coef_x}x"
            ans_y = "" if coef_y == 0 else "+y" if coef_y == 1 else "-y" if coef_y == -1 else f"+{coef_y}y" if (coef_y > 0) and (coef_x != 0) else f"{coef_y}y"
            ans_c = "" if coef_c == 0 else f"+{coef_c}" if (coef_c > 0) and (ans_x + ans_y != "") else str(coef_c)
            answer = f"{ans_x}{ans_y}{ans_c}"
            answer = "0" if answer == "" else answer

            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return AlgebraicSimplificationPlugin()