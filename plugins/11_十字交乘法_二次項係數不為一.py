from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class CrossMultiplyQuadA1Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "十字交乘法因式分解（二次項係數不為 1）"

    def generate(self, count):
        # 此題型專注於整數因式分解，若 UI 選擇非整數格式則退回到整數模式
        number_format = getattr(self, "number_format", "integer")
        if number_format != "integer":
            number_format = "integer"

        amplitude = getattr(self, "amplitude", 10)

        num_gen = NumberGenerator(
            number_format=number_format,
            amplitude=amplitude,
            decimal_places=2,
            allow_negative=True,
            fraction_simplify=True,
        )

        results = []
        for _ in range(count):
            # 產生 4 個整數
            m, m_text = num_gen.generate()
            n, n_text = num_gen.generate()
            p, p_text = num_gen.generate()
            q, q_text = num_gen.generate()

            while 0 in [m, n, p, q]:
                m, m_text = num_gen.generate()
                n, n_text = num_gen.generate()
                p, p_text = num_gen.generate()
                q, q_text = num_gen.generate()

            # 化簡 m, p 與 n, q 的最大公因數
            from math import gcd
            gcd_m_p = gcd(abs(m), abs(p))
            if gcd_m_p > 1:
                m //= gcd_m_p
                p //= gcd_m_p
            gcd_n_q = gcd(abs(n), abs(q))
            if gcd_n_q > 1:
                n //= gcd_n_q
                q //= gcd_n_q
            a = m * n
            b = m * q + n * p
            c = p * q

            # 組出題目字串，處理正負號顯示
            a_part = f"x^2" if a == 1 else f"-x^2" if a == -1 else f"{a}x^2"
            b_part = f"+x" if b == 1 else f"-x" if b == -1 else f"+{b}x" if b > 0 else "" if b == 0 else f"{b}x"
            c_part = f"+{c}" if c > 0 else str(c)

            # 特殊情況：若 b == 0 或 c == 0，確保形式正確（例如 x^2+0x+3 -> x^2+3）
            question = f"{a_part}{b_part}{c_part}"
            # 組答案 (mx + p)(nx + q)
            term_1 = f"({'' if m == 1 else '-' if m == -1 else m}x{'+' if p >= 0 else ''}{p})"
            term_2 = f"({'' if n == 1 else '-' if n == -1 else n}x{'+' if q >= 0 else ''}{q})"
            answer = f"{term_1}{term_2}"

            results.append((format_latex(question), format_latex(answer)))

        return results


def get_plugin():
    return CrossMultiplyQuadA1Plugin()
