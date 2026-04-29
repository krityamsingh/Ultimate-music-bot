# ============================================================
#  handlers/__init__.py  —  Auto-loader
#
#  Add a new feature: just create handlers/myfeature.py
#  with a  def register(bot, userbot):  function.
# ============================================================

import importlib
import pkgutil
from pathlib import Path


def load_all(bot, userbot):
    package_dir  = Path(__file__).parent
    package_name = __name__

    loaded  = []
    skipped = []

    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module_name = f"{package_name}.{module_info.name}"
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"[handlers] ⚠️  Could not import {module_name}: {e}")
            continue

        if hasattr(module, "register"):
            try:
                module.register(bot, userbot)
                loaded.append(module_info.name)
            except Exception as e:
                print(f"[handlers] ⚠️  register() failed in {module_name}: {e}")
        else:
            skipped.append(module_info.name)

    print(f"[handlers] ✅ Loaded : {loaded}")
    if skipped:
        print(f"[handlers] ⏭  Skipped: {skipped}  (no register() found)")
