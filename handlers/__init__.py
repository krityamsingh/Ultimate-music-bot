# ============================================================
#  handlers/__init__.py
#
#  Auto-loader: scans this package for every module that
#  exposes a  register(bot, userbot)  function and calls it.
#
#  ✅ To add a new feature later:
#     1. Create  handlers/myfeature.py
#     2. Define  def register(bot, userbot): ...  inside it
#     3. That's it — nothing else to touch.
# ============================================================

import importlib
import pkgutil
from pathlib import Path


def load_all(bot, userbot):
    """
    Dynamically import every module inside the handlers/ package
    and call its register(bot, userbot) function if it exists.
    """
    package_dir = Path(__file__).parent
    package_name = __name__  # "handlers"

    loaded = []
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

    print(f"[handlers] ✅ Loaded   : {loaded}")
    if skipped:
        print(f"[handlers] ⏭  Skipped  : {skipped}  (no register() found)")
