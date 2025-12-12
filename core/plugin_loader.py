import importlib.util
import os
import sys
from PyQt5.QtWidgets import (
    QMessageBox,
)

class PluginManager:
    def __init__(self, plugin_dir=None):
        if getattr(sys, 'frozen', False):
            # 當以 PyInstaller 打包為 single-file 時，資源會解壓到 sys._MEIPASS
            # 優先使用 exe 旁可修改的 plugins 資料夾（支援熱插拔），若不存在再回退到 sys._MEIPASS
            exe_dir = os.path.dirname(sys.executable)
            external_plugins = os.path.join(exe_dir, "plugins")
            if os.path.exists(external_plugins):
                base_path = exe_dir
            else:
                base_path = getattr(sys, '_MEIPASS', exe_dir)
        else:
            # 非 frozen 時，專案根目錄為 core/ 的上層目錄
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # 將專案根目錄加入 sys.path，讓 plugin 可以 import core.*
        core_path = os.path.abspath(base_path)
        if core_path not in sys.path:
            sys.path.insert(0, core_path)

        if plugin_dir is None:
            # 若為 frozen 且 exe 旁存在 plugins 資料夾，使用該資料夾以支援熱插拔；
            # 否則使用 base_path 下的 plugins（對開發環境或 bundle 中的資源適用）
            candidate = os.path.join(base_path, "plugins")
            if getattr(sys, 'frozen', False):
                exe_plugins = os.path.join(os.path.dirname(sys.executable), "plugins")
                if os.path.exists(exe_plugins):
                    plugin_dir = exe_plugins
                else:
                    plugin_dir = candidate
            else:
                plugin_dir = candidate

        self.plugin_dir = os.path.abspath(plugin_dir)
        self.plugins = []

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            # print(f"Plugin 資料夾不存在：{self.plugin_dir}")
            QMessageBox.critical(
                None,
                "錯誤",
                f"Plugin 資料夾不存在：{self.plugin_dir}",
            )
            return
        
        core_parent = os.path.abspath(os.path.join(self.plugin_dir, ".."))
        if core_parent not in sys.path:
            sys.path.insert(0, core_parent)

        # 如果為 frozen，將解壓目錄加入 sys.path，並將 plugins 目錄注入為 package
        if getattr(sys, 'frozen', False):
            meipass = getattr(sys, '_MEIPASS', None)
            if meipass and meipass not in sys.path:
                sys.path.insert(0, meipass)

        package_name = "plugins"
        try:
            import types
            if package_name not in sys.modules:
                pkg = types.ModuleType(package_name)
                pkg.__path__ = [self.plugin_dir]
                sys.modules[package_name] = pkg
        except Exception:
            pass

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                path = os.path.join(self.plugin_dir, filename)
                name = os.path.splitext(filename)[0]
                # 使用 package-qualified module name，讓 plugin 的 imports 正確解析
                full_name = f"{package_name}.{name}"
                spec = importlib.util.spec_from_file_location(full_name, path)
                module = importlib.util.module_from_spec(spec)
                # 設定 __package__ 以利內部 import
                try:
                    module.__package__ = package_name
                except Exception:
                    pass
                spec.loader.exec_module(module)

                # 要求 plugin module 有 get_plugin() 函數，回傳 class 實例
                if hasattr(module, "get_plugin"):
                    try:
                        plugin_instance = module.get_plugin()
                        self.plugins.append(plugin_instance)
                    except Exception:
                        # 不讓單一 plugin 失敗影響整體載入
                        continue
                elif name == "__init__" or name == "general":
                    continue
                else:
                    QMessageBox.warning(
                        None,
                        "警告",
                        f"Plugin '{name}' 缺少 get_plugin() 函數，已跳過",
                    )
    
    def get_plugins(self):
        return self.plugins
