

import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "app"
)
sys.path.append(SOURCE_PATH)

os.chdir("app")
