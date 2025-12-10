from fractions import Fraction
from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class Equation3Plugin(BasePlugin):
    def __init__(self, amplitude=100):
        self.amplitude = amplitude

    def get_name(self):
        return "一元一次方程式(ax+b=c)"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b, c = generate_nums(3, self.amplitude)
            while (a in [0, 1]) or (b == 0):
                a, b, c = generate_nums(3, self.amplitude)

            question = f"{a}x+{b}={c}" if b > 0 else f"{a}x{b}={c}"
            answer = f"{(c - b) // a}" if (c - b) % a == 0 else None
            if answer is None:
                frac = Fraction(c - b, a)
                answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation3Plugin()