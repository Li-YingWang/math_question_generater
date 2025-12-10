from fractions import Fraction
from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class Equation2Plugin(BasePlugin):
    def __init__(self, amplitude=100):
        self.amplitude = amplitude

    def get_name(self):
        return "一元一次方程式(ax=b)"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b = generate_nums(2, self.amplitude)
            while (a in [0, 1]) or (b == 0):
                a, b = generate_nums(2, self.amplitude)

            question = f"{a}x={b}"
            answer = f"{b // a}" if b % a == 0 else None
            if answer is None:
                frac = Fraction(b, a)
                answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation2Plugin()