from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

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

            coef_x = g * a + h * d
            coef_y = g * b + h * e
            coef_c = g * c + h * f
            ans_x = "" if coef_x == 0 else "x" if coef_x == 1 else "-x" if coef_x == -1 else f"{coef_x}x" if coef_x > 0 else f"{coef_x}x"
            ans_y = "" if coef_y == 0 else "+y" if coef_y == 1 else "-y" if coef_y == -1 else f"+{coef_y}y" if (coef_y > 0) and (ans_x != "") else f"{coef_y}y"
            ans_c = "" if coef_c == 0 else f"+{coef_c}" if (coef_c > 0) and (ans_x + ans_y != "") else str(coef_c)
            answer = f"{ans_x}{ans_y}{ans_c}"
            answer = "0" if answer == "" else answer

            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return AlgebraicSimplificationPlugin()