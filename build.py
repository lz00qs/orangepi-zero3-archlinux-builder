# -*- coding: utf-8 -*-
# 检查Python版本
import configparser
from tools import Logger
import os
import subprocess
import sys
from tools import clone_to_dir, download_to_dir, extract_to_dir, run_relative_shell

if sys.version_info < (3, 6):
    print("Python 3.6+ is required.")
    sys.exit(1)

os.environ["global_log_level"] = 'DEBUG'

logger = Logger(name="log")

logger.info("Python version satisfied, colorlog installed.")

system_info = os.uname()
host_arch = system_info.machine
logger.info(f"Host arch: {host_arch}")
cross_flag = False
if host_arch == "x86_64":
    cross_flag = True
    os.environ["CROSS"] = "True"


config = configparser.ConfigParser()
config.read('config.ini')

path_base = os.getcwd()
os.environ["PATH_BASE"] = path_base

path_build = os.path.join(path_base, "build")
os.environ["PATH_BUILD"] = path_build
if not os.path.exists(path_build):
    os.mkdir(path_build)

path_build_resources = os.path.join(path_build, "resources")
os.environ["PATH_BUILD_RESOURCES"] = path_build_resources
if not os.path.exists(path_build_resources):
    os.mkdir(path_build_resources)

path_build_root = os.path.join(path_build, "build_root")
os.environ["PATH_BUILD_ROOT"] = path_build_root
if not os.path.exists(path_build_root):
    os.mkdir(path_build_root)

path_build_toolchains = os.path.join(path_build, "toolchains")
os.environ["PATH_BUILD_TOOLCHAINS"] = path_build_toolchains
if not os.path.exists(path_build_toolchains):
    os.mkdir(path_build_toolchains)

path_build_toolchains_xtools = os.path.join(path_build_toolchains, "xtools")
os.environ["PATH_BUILD_TOOLCHAINS_XTOOLS"] = path_build_toolchains_xtools
if not os.path.exists(path_build_toolchains_xtools):
    os.mkdir(path_build_toolchains_xtools)

path_scripts_in = os.path.join(path_base, "scripts/in")
os.environ["PATH_SCRIPTS_IN"] = path_scripts_in

try:
    subprocess.run("python3 prepare_build_root.py", shell=True, check=True)
except Exception as e:
    logger.error("Prepare build root failed.")
    sys.exit(1)

try:
    subprocess.run("python3 prepare_xtools.py", shell=True, check=True)
except Exception as e:
    logger.error("Prepare xtools failed.")
    sys.exit(1)
