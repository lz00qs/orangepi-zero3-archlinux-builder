# -*- coding: utf-8 -*-
from datetime import datetime
from scripts.out.py_modules.tools import Logger, run_relative_shell, prepare_config, restore_config
import configparser
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Build options parser')
parser.add_argument('--build', choices=['pkg', 'rootfs', 'img'], default='img', help='Build option')

build_option = parser.parse_args().build
os.environ["build_option"] = build_option

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

path_pkg_built = os.path.join(path_base, "pkg_built")
os.environ["PATH_PKG_BUILT"] = path_pkg_built
if not os.path.exists(path_pkg_built):
    os.mkdir(path_pkg_built)

path_releases = os.path.join(path_base, "releases")
os.environ["PATH_RELEASES"] = path_releases
if not os.path.exists(path_releases):
    os.mkdir(path_releases)
    
os.environ["PATH_PACSTRAP_ROOTFS"] = os.path.join(path_build_root, "home/alarm/build/pacstrap_rootfs")

os.environ["PKGEXT"] = ".pkg.tar"

try:
    prepare_config(os.path.join(path_base, "config.ini"))
    config = configparser.ConfigParser()
    config.read('config.ini')
    release_prefix = config.get('ReleaseConfig', 'release_prefix')
    release_prefix = f"{release_prefix}-" + datetime.now().strftime("%Y%m%d%H%M%S")
    os.environ["RELEASE_PREFIX"] = release_prefix
    if os.path.exists(path_build_root):
        from scripts.out.py_modules.prepare import prepare_build_root
        prepare_build_root()

    if cross_flag:
        from scripts.out.py_modules.prepare import prepare_xtools
        prepare_xtools()

    run_relative_shell(os.path.join(path_scripts_out, "download_pkg.sh"))

    if cross_flag:
        run_relative_shell(os.path.join(path_scripts_out, "cross_build_pkg.sh"))

    import scripts.out.py_modules as modules
    modules.build_in_chroot()
except Exception as e:
    logger.error(e)
    sys.exit(1)
finally:
    restore_config(os.path.join(path_base, "config.ini"))
