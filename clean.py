import os
import sys
from scripts.out.py_modules.tools import Logger
logger = Logger(name="log")

logger.info("Cleaning...")

if os.path.exists("pkg_built"):
    logger.info("Removing pkg_built...")
    os.system("rm -rf pkg_built")

if os.path.exists("build"):
    logger.info("Removing build...")
    os.system("sudo rm -rf build")

if os.path.exists("releases"):
    logger.info("Removing releases...")
    os.system("sudo rm -rf releases")

for root, dirs, files in os.walk("pkg_cross"):
    for file in files:
        if file.endswith(".tar"):
            file_path = os.path.join(root, file)
            try:
                os.system(f"sudo rm -f {file_path}")
            except Exception as e:
                logger.error("Remove file error. " + e.__str__())
                sys.exit(1)
