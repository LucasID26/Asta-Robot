from . import plugins

import importlib
import os

def check_plugins():
  with open('Asta/plugins/__init__.py', 'r') as f:
    init_lines = f.readlines()

  teks = ""
  for file in os.listdir('Asta/plugins'):
    if file.endswith('.py') and not file.startswith('__'):
      module_name = file[:-3]
      if module_name not in sys.modules:
        importlib.import_module(module_name)
        teks += f"- `{module_name}`\n")
        import_line = f"from . import {module_name}\n"
        if import_line not in init_lines:
          with open('Asta/plugins/__init__.py', 'a') as f:
            f.write(import_line)
  return teks
