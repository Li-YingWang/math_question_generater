import os
import sys


# 在載入 PyQt5 之前嘗試設定 Qt 平台 plugin 路徑，避免找不到 qwindows.dll 的錯誤
def _set_qt_plugin_path():
    base = os.path.dirname(os.path.abspath(__file__))

    # 1) 嘗試專案虛擬環境常見路徑
    venv_plugins = os.path.join(base, ".venv", "Lib", "site-packages", "PyQt5", "Qt5", "plugins", "platforms")
    if os.path.exists(venv_plugins):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = venv_plugins
        return

    # 2) 嘗試使用已安裝 PyQt5 的實際位置
    try:
        import importlib.util
        spec = importlib.util.find_spec("PyQt5")
        if spec and spec.origin:
            pyqt_base = os.path.dirname(spec.origin)
            plugins = os.path.join(pyqt_base, "Qt5", "plugins", "platforms")
            if os.path.exists(plugins):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugins
                return
    except Exception:
        pass


_set_qt_plugin_path()

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
