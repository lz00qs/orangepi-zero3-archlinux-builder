# -*- coding: utf-8 -*-
from scripts.out.py_modules.tools import Logger, run_relative_shell, prepare_config, restore_config
import configparser
import os
import sys

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

os.environ["PATH_SCRIPTS"] = os.path.join(path_base, "scripts")
os.environ["PATH_SCRIPTS_IN"] = os.path.join(path_base, "scripts/in")
path_scripts_out = os.path.join(path_base, "scripts/out")
os.environ["PATH_SCRIPTS_OUT"] = path_scripts_out
os.environ["PATH_PKG"] = os.path.join(path_base, "pkg")
os.environ["PATH_PKG_CROSS"] = os.path.join(path_base, "pkg_cross")
os.environ["PATH_PKG_BUILT"] = os.path.join(path_base, "pkg_built")

os.environ["PKGEXT"] = ".pkg.tar"

try:
    prepare_config(os.path.join(path_base, "config.ini"))
    if os.path.exists(path_build_root):
        from scripts.out.py_modules.prepare import prepare_build_root
        prepare_build_root()

    if cross_flag:
        from scripts.out.py_modules.prepare import prepare_xtools
        prepare_xtools()

    run_relative_shell(os.path.join(path_scripts_out, "download_pkg.sh"))

    run_relative_shell(os.path.join(path_scripts_out, "cross_build_pkg.sh"))

    import scripts.out.py_modules as modules
    modules.build_in_chroot()
except Exception as e:
    logger.error(e)
    sys.exit(1)
finally:
    restore_config(os.path.join(path_base, "config.ini"))
