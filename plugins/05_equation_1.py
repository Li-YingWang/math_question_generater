from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class Equation1Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "一元一次方程式(x+a=b)"

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
            while a == 0:
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()

            question = f"x+{a_text}={b_text}" if a > 0 else f"x{a_text}={b_text}"
            if number_format == "fraction":
                from fractions import Fraction
                frac = Fraction(b - a)
                if frac.denominator == 1:
                    answer = str(frac.numerator)
                elif frac.numerator < 0:
                    answer = f"-\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}"
                else:
                    answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            elif number_format == "decimal":
                answer = f"{round(b - a, 2):.2f}"
            else:
                answer = str(b - a)
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation1Plugin()