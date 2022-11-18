##Build.py
from TouchPortalAPI import tppbuild
import json
import os


PLUGIN_MAIN = "main.py"


PLUGIN_EXE_NAME = "DataParser"
PLUGIN_EXE_ICON = "


PLUGIN_ENTRY = "entry.tp"  # Here we just use the same file as the plugin's main code since that contains all the definitions for entry.tp.
PLUGIN_ENTRY_INDENT = 2
PLUGIN_ROOT = "DataParser"
PLUGIN_ICON = ""


OUTPUT_PATH = r"./"



entry = os.path.join(os.path.split(__file__)[0], PLUGIN_ENTRY)
with open(entry, "r") as f:
    PLUGIN_VERSION = str(json.load(f)['version'])


ADDITIONAL_FILES = [
    "start.sh"
    ]


ADDITIONAL_PYINSTALLER_ARGS = [
    "--noconsole"
   # "--log-level=WARN"
]

ADDITIONAL_TPPSDK_ARGS = []
# validateBuild()

if __name__ == "__main__":
    tppbuild.runBuild()
