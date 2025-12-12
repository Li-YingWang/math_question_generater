from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin
from fractions import Fraction

class AlgebraicSimplificationPlugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "代數式化簡"

    def generate(self, count):
        number_format = getattr(self, "number_format", "integer")
        amplitude = getattr(self, "amplitude", 10)
        returns = []
        for _ in range(count):
            num_gen = NumberGenerator(
                number_format=number_format,
                amplitude=amplitude,
                decimal_places=2,
                allow_negative=True,
                fraction_simplify=True
            )
            nums = []
            for _ in range(8):
                n, n_text = num_gen.generate()
                nums.append((n, n_text))
            a, a_text = nums[0]
            b, b_text = nums[1]
            c, c_text = nums[2]
            d, d_text = nums[3]
            e, e_text = nums[4]
            f, f_text = nums[5]
            g, g_text = nums[6]
            h, h_text = nums[7]
            
            while (0 in [a, b, c, d, e, f, g, h]):
                nums = []
                for _ in range(8):
                    n, n_text = num_gen.generate()
                    nums.append((n, n_text))
                a, a_text = nums[0]
                b, b_text = nums[1]
                c, c_text = nums[2]
                d, d_text = nums[3]
                e, e_text = nums[4]
                f, f_text = nums[5]
                g, g_text = nums[6]
                h, h_text = nums[7]

            x1 = "x" if a == 1 else "-x" if a == -1 else f"{a_text}x"
            y1 = "+y" if b == 1 else "-y" if b == -1 else f"+{b_text}y" if b > 0 else f"{b_text}y"
            c1 = f"+{c_text}" if c > 0 else c_text
            x2 = "x" if d == 1 else "-x" if d == -1 else f"{d_text}x"
            y2 = "+y" if e == 1 else "-y" if e == -1 else f"+{e_text}y" if e > 0 else f"{e_text}y"
            c2 = f"+{f_text}" if f > 0 else f_text
            m = "" if g == 1 else "-" if g == -1 else f"{g_text}" if g > 0 else g_text
            n = "+" if h == 1 else "-" if h == -1 else f"+{h_text}" if h > 0 else h_text
            question = f"{m}({x1}{y1}{c1}){n}({x2}{y2}{c2})"

            coef_x = Fraction(g * a + h * d)
            coef_y = Fraction(g * b + h * e)
            coef_c = Fraction(g * c + h * f)

            if number_format == "integer":
                coef_x_text = coef_x.numerator
                coef_y_text = coef_y.numerator
                coef_c_text = coef_c.numerator
            elif number_format == "fraction":
                coef_x_text = coef_x.numerator if coef_x.denominator == 1 else f"-\\frac{{{abs(coef_x.numerator)}}}{{{coef_x.denominator}}}" if coef_x < 0 else f"\\frac{{{coef_x.numerator}}}{{{coef_x.denominator}}}"
                coef_y_text = coef_y.numerator if coef_y.denominator == 1 else f"-\\frac{{{abs(coef_y.numerator)}}}{{{coef_y.denominator}}}" if coef_y < 0 else f"\\frac{{{coef_y.numerator}}}{{{coef_y.denominator}}}"
                coef_c_text = coef_c.numerator if coef_c.denominator == 1 else f"-\\frac{{{abs(coef_c.numerator)}}}{{{coef_c.denominator}}}" if coef_c < 0 else f"\\frac{{{coef_c.numerator}}}{{{coef_c.denominator}}}"
            else:
                coef_x_text = round(float(coef_x), 4)
                coef_y_text = round(float(coef_y), 4)
                coef_c_text = round(float(coef_c), 4)
            ans_x = "" if coef_x == 0 else "x" if coef_x == 1 else "-x" if coef_x == -1 else f"{coef_x_text}x" if coef_x > 0 else f"{coef_x_text}x"
            ans_y = "" if coef_y == 0 else "+y" if coef_y == 1 else "-y" if coef_y == -1 else f"+{coef_y_text}y" if (coef_y > 0) and (ans_x != "") else f"{coef_y_text}y"
            ans_c = "" if coef_c == 0 else f"+{coef_c_text}" if (coef_c > 0) and (ans_x + ans_y != "") else coef_c_text
            answer = f"{ans_x}{ans_y}{ans_c}"
            answer = "0" if answer == "" else answer

            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return AlgebraicSimplificationPlugin()