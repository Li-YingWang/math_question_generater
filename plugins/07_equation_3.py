from fractions import Fraction
from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class Equation3Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "一元一次方程式(ax+b=c)"

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
            c, c_text = num_gen.generate()
            while (a in [0, 1]) or (b == 0):
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()
                c, c_text = num_gen.generate()

            question = f"{"" if a == 1 else "-" if a == -1 else f"{a_text}"}x+{b_text}={c_text}" if b > 0 else f"{a_text}x{b_text}={c_text}"
            if number_format == "decimal":
                ans_num = round(100 * (c - b))
                ans_dec = round(100 * a)
                ans = Fraction(ans_num, ans_dec)
            else:
                ans = Fraction((c - b), a)
            if ans.denominator == 1:
                answer = f"{ans.numerator}"
            elif ans.numerator < 0:
                answer = f"-\\frac{{{abs(ans.numerator)}}}{{{ans.denominator}}}"
            else:
                answer = f"\\frac{{{ans.numerator}}}{{{ans.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation3Plugin()