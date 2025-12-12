from fractions import Fraction
from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class Equation2Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "一元一次方程式(ax=b)"

    def generate(self, count):
        number_format = getattr(self, "number_format", "integer")
        amplitude = getattr(self, "amplitude", 100)
        returns = []
        for _ in range(count):
            num_gen = NumberGenerator(
                number_format=number_format,
                amplitude=amplitude,
                decimal_places=2,
                allow_negative=True,
                fraction_simplify=True
            )
            a, a_text = num_gen.generate()
            b, b_text = num_gen.generate()
            while (a in [0, 1]) or (b == 0):
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()

            question = f"{a_text}x={b_text}"
            if number_format == "decimal":
                ans_num = round(100 * b)
                ans_dec = round(100 * a)
                ans = Fraction(ans_num, ans_dec)
            else:
                ans = Fraction(b, a)
            if ans.denominator == 1:
                answer = f"{ans.numerator}"
            elif ans.numerator < 0:
                answer = f"-\\frac{{{abs(ans.numerator)}}}{{{ans.denominator}}}"
            else:
                answer = f"\\frac{{{ans.numerator}}}{{{ans.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation2Plugin()