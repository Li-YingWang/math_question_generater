from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class MultiplicationPlugin(BasePlugin):
    def __init__(self, amplitude=100):
        self.amplitude = amplitude

    def get_name(self):
        return "整數乘法(國中)"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b = generate_nums(2, self.amplitude)
            while (a >= 0) and (b >= 0):
                a, b = generate_nums(2, self.amplitude)

            str_a = f"({a})" if a < 0 else str(a)
            str_b = f"({b})" if b < 0 else str(b)

            question = str_a + " \\times " + str_b
            answer = str(a * b)
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return MultiplicationPlugin()