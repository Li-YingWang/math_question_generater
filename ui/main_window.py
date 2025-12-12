# ui/main_window.py

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QPushButton, QMessageBox, QTextEdit, QSpinBox, QComboBox,
    QSlider,
)
from PyQt5.QtCore import Qt
import time
import subprocess
import os
import glob

from core.plugin_loader import PluginManager
from core.generate_latex import LatexBuilder




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        self.plugins = self.plugin_manager.get_plugins()
        layout = QVBoxLayout()

        # 顯示目前加入的題目
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # 控制列：題型、數字形式、題數、加入按鈕
        controls = QHBoxLayout()

        controls.addWidget(QLabel("題型："))
        self.plugin_combo = QComboBox()
        for plugin in self.plugins:
            try:
                name = plugin.get_name()
            except Exception:
                name = getattr(plugin, "__class__", type(plugin)).__name__
            self.plugin_combo.addItem(name)
        controls.addWidget(self.plugin_combo)

        controls.addWidget(QLabel("數字形式："))
        self.format_combo = QComboBox()
        # 顯示中文但用 internal values
        self.format_map = {"整數": "integer", "分數": "fraction", "小數": "decimal"}
        for k in self.format_map.keys():
            self.format_combo.addItem(k)
        controls.addWidget(self.format_combo)

        self.slider_amplitude = QSlider()
        self.slider_amplitude.setOrientation(Qt.Horizontal)
        self.slider_amplitude.setRange(1, 100)
        self.slider_amplitude.setValue(100)

        # 新增一個數字輸入框，讓使用者可手動輸入 amplitude，並與滑桿同步
        self.amplitude_spin = QSpinBox()
        self.amplitude_spin.setRange(1, 100)
        self.amplitude_spin.setValue(self.slider_amplitude.value())
        self.amplitude_spin.setFixedWidth(80)

        controls.addWidget(QLabel("數字範圍："))
        controls.addWidget(self.slider_amplitude)
        controls.addWidget(QLabel("±"))
        controls.addWidget(self.amplitude_spin)

        # 同步：滑桿改變更新標籤與 spinbox；spinbox 改變也會設定滑桿
        self.slider_amplitude.valueChanged.connect(self.amplitude_spin.setValue)
        self.amplitude_spin.valueChanged.connect(self.slider_amplitude.setValue)
        controls.addWidget(QLabel("題數："))
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 500)
        self.count_spin.setValue(10)
        self.count_spin.setFixedWidth(80)
        controls.addWidget(self.count_spin)

        self.add_button = QPushButton("加入題目")
        self.add_button.clicked.connect(self.add_questions)
        controls.addWidget(self.add_button)

        layout.addLayout(controls)

        # 用來儲存目前的題目與答案（平坦列表，稍後會分頁）
        self.qa_pairs = []

        # 匯出按鈕
        self.pdf_button = QPushButton("匯出 LATEX & PDF")
        self.pdf_button.clicked.connect(self.export_pdf)
        layout.addWidget(self.pdf_button)

        self.setLayout(layout)

    def add_questions(self):
        # 根據目前的選項產生題目並加入到 qa_pairs
        idx = self.plugin_combo.currentIndex()
        if idx < 0 or idx >= len(self.plugins):
            QMessageBox.warning(self, "錯誤", "請先選擇題型")
            return

        plugin = self.plugins[idx]
        fmt_display = self.format_combo.currentText()
        number_format = self.format_map.get(fmt_display, "integer")

        count = int(self.count_spin.value())

        # 把使用者選的 number_format 設定到 plugin（若 plugin 使用會讀取）
        try:
            setattr(plugin, "number_format", number_format)
            # 將 amplitude 傳給 plugin（plugin 若需要可讀取此屬性）
            amplitude = int(self.slider_amplitude.value())
            setattr(plugin, "amplitude", amplitude)
            q_a_pairs = plugin.generate(count)
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"產生題目失敗：{e}")
            return

        # 加入主題庫並更新顯示
        self.qa_pairs.extend(q_a_pairs)
        for q, a in q_a_pairs:
            self.result_display.append(f"題目: {q}  答案: {a}")

    def generate_latex(self):
        if not self.qa_pairs:
            raise RuntimeError("目前沒有題目，請先加入題目再匯出")

        # 確保 output 目錄存在
        os.makedirs("output", exist_ok=True)
        
        output_path = f"output/output_{time.strftime('%Y%m%d_%H%M%S')}.tex"
        template_path = "templates/template.tex"

        # 依照每頁最多 10 題分割（與 LatexBuilder 的預期資料結構相容）
        chunk_size = 20
        pages = [self.qa_pairs[i:i+chunk_size] for i in range(0, len(self.qa_pairs), chunk_size)]

        latex_builder = LatexBuilder(template_path, output_path)
        tex_path = latex_builder.build_latex_content(pages)

        # 取得檔名（不含路徑）用於在 output 目錄執行編譯
        tex_filename = os.path.basename(tex_path)
        
        # 先清理舊的中間檔（防止被鎖定）
        base_name = os.path.splitext(tex_filename)[0]
        try:
            for pattern in [f"output/{base_name}.*"]:
                for f in glob.glob(pattern):
                    if not f.endswith('.tex'):
                        try:
                            os.remove(f)
                        except Exception:
                            pass
        except Exception:
            pass
        
        # 再編譯 PDF（在 output 目錄執行、強制編譯、不暫停於錯誤）
        try:
            result = subprocess.run(
                ["latexmk", "-f", "-xelatex", "-interaction=nonstopmode", tex_filename],
                cwd="output",
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode != 0:
                error_msg = result.stderr if result.stderr else result.stdout
                # 嘗試從 log 檔找出實際錯誤
                log_file = f"output/{base_name}.log"
                if os.path.exists(log_file):
                    try:
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            log_content = f.read()
                            # 找出 Error 行
                            for line in log_content.split('\n'):
                                if 'Error' in line or 'error' in line:
                                    error_msg = line
                                    break
                    except Exception:
                        pass
                raise RuntimeError(f"LaTeX 編譯失敗 (exit code {result.returncode}):\n{error_msg}")
        except FileNotFoundError:
            raise RuntimeError("找不到 latexmk，請確認已安裝 TeX Live 或 MiKTeX")
        except subprocess.TimeoutExpired:
            raise RuntimeError("LaTeX 編譯超時（超過 120 秒）")

        # 清理中間檔（輸出 PDF 之後）
        try:
            subprocess.run(
                ["latexmk", "-c", tex_filename],
                cwd="output",
                capture_output=True,
                timeout=30
            )
        except Exception:
            pass  # 清理失敗不打斷流程

    def export_pdf(self):

        try:
            self.pdf_button.setText("匯出中...")
            self.pdf_button.setEnabled(False)
            QApplication.processEvents()  # 強制刷新畫面

            self.generate_latex()

            QMessageBox.information(self, "成功", "PDF 產生成功！\n\n輸出檔案位於 output/ 資料夾")
        except Exception as e:
            error_details = str(e)
            QMessageBox.critical(self, "錯誤", f"PDF 產生失敗：\n\n{error_details}")
        finally:
            self.pdf_button.setText("匯出 LATEX & PDF")
            self.pdf_button.setEnabled(True)
