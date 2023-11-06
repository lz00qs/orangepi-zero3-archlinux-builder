import configparser
import os
import subprocess
import sys
from tools import extract_to_dir, download_to_dir

from tools import Logger
logger = Logger(name="log")

path_build_resources = os.environ["PATH_BUILD_RESOURCES"]
path_build_toolchains_xtools = os.environ["PATH_BUILD_TOOLCHAINS_XTOOLS"]


config = configparser.ConfigParser()
config.read('config.ini')

logger.info("Start preparing xtools!")

prepared_mark = os.path.join(path_build_toolchains_xtools, ".prepared")

if not os.path.exists(prepared_mark):
    url = config.get('UrlConfig', 'xtools_url')
    download_to_dir(url, path_build_resources,
                    'xtools_aarch64_on_x86_64.tar.xz')
    try:
        extract_to_dir(f"sudo bsdtar -C {path_build_toolchains_xtools} --acls --xattrs --strip-components 1 -xpf "
                       + os.path.join(path_build_resources, "xtools_aarch64_on_x86_64.tar.xz"), path_build_toolchains_xtools)
        subprocess.run(f"sudo touch {prepared_mark}", shell=True, check=True)
        logger.info("Prepare xtools finished!")
    except Exception as e:
        logger.error("Prepare xtools failed." + e)
        sys.exit(1)
else:
    logger.info("Xtools already prepared.")
