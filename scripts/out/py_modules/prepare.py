import os
import sys
import configparser
import subprocess

# from tools import clone_to_dir, download_to_dir, extract_to_dir, run_relative_shell, Logger
from scripts.out.py_modules.tools import extract_to_dir, download_to_dir, Logger
logger = Logger(name="log")

path_build_resources = os.environ["PATH_BUILD_RESOURCES"]
path_build_root = os.environ["PATH_BUILD_ROOT"]
path_scripts_in = os.environ["PATH_SCRIPTS_IN"]
path_build_toolchains_xtools = os.environ["PATH_BUILD_TOOLCHAINS_XTOOLS"]


def prepare_build_root():
    prepared_mark = os.path.join(path_build_root, ".prepared")
    if not os.path.exists(prepared_mark):
        logger.info("Start preparing build root")
        config = configparser.ConfigParser()
        config.read('config.ini')
        url = config.get('UrlConfig', 'arch_aarch64_rootfs_url')
        download_to_dir(url, path_build_resources, 'aarch64_rootfs.tar.gz')
        try:
            subprocess.run(
                "sudo -E python3 scripts/out/py_modules/extract_build_root.py", shell=True, check=True)
            mirror_url = url = config.get('PacManConfig', 'mirror_url')
            if mirror_url:
                old_url = 'http://mirror.archlinuxarm.org/$arch/$repo'
                mirrorlist_path = os.path.join(
                    path_build_root, "etc/pacman.d/mirrorlist")
                cmd = f"sudo sed -i 's#{old_url}#{mirror_url}#g' {mirrorlist_path}"
                try:
                    subprocess.run(cmd, shell=True, check=True)
                    logger.info(
                        f"Changed mirror url to {mirror_url} in {mirrorlist_path}")
                except subprocess.CalledProcessError as e:
                    logger.warning(
                        f"Failed to change mirror url to {mirror_url} in {mirrorlist_path}")
            path_entry_script_in = '/root/prepare_build_root_entrypoint.sh'
            path_entry_script_in_absolute = f"{path_build_root}{path_entry_script_in}"
            path_entry_script_out = os.path.join(
                path_scripts_in, "prepare_build_root_entrypoint.sh")
            subprocess.run(
                f"sudo install -Dm755 \"{path_entry_script_out}\" \"{path_entry_script_in_absolute}\"", shell=True, check=True)
            subprocess.run(
                f"sudo mount -o bind \"{path_build_root}\" \"{path_build_root}\"", shell=True, check=True)
            subprocess.run(
                f"sudo arch-chroot \"{path_build_root}\" \"{path_entry_script_in}\"", shell=True, check=True)
            subprocess.run(
                f"sudo umount \"{path_build_root}\"", shell=True, check=True)
            subprocess.run(
                f"sudo rm -f {path_entry_script_in_absolute}", shell=True, check=True)
            subprocess.run(
                f"sudo touch {prepared_mark}", shell=True, check=True)
            logger.info("Prepare build root finished!")
        except Exception as e:
            logger.error("Prepare build root error. " + e)
            sys.exit(1)
    else:
        logger.info("Build root already prepared.")


def prepare_xtools():
    prepared_mark = os.path.join(path_build_toolchains_xtools, ".prepared")
    if not os.path.exists(prepared_mark):
        logger.info("Start preparing xtools")
        config = configparser.ConfigParser()
        config.read('config.ini')
        url = config.get('UrlConfig', 'xtools_url')
        download_to_dir(url, path_build_resources,
                        'xtools_aarch64_on_x86_64.tar.xz')
        try:
            extract_to_dir(f"sudo bsdtar -C {path_build_toolchains_xtools} --acls --xattrs --strip-components 1 -xpf "
                           + os.path.join(path_build_resources, "xtools_aarch64_on_x86_64.tar.xz"), path_build_toolchains_xtools)
            subprocess.run(
                f"sudo touch {prepared_mark}", shell=True, check=True)
            logger.info("Prepare xtools finished!")
        except Exception as e:
            logger.error("Prepare xtools error. " + e)
            sys.exit(1)
    else:
        logger.info("Xtools already prepared.")
