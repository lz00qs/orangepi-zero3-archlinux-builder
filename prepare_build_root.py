import os
import sys
import configparser
import subprocess

from tools import clone_to_dir, download_to_dir, extract_to_dir, run_relative_shell, Logger
logger = Logger(name="log")

path_build_resources = os.environ["PATH_BUILD_RESOURCES"]
path_build_root = os.environ["PATH_BUILD_ROOT"]
path_scripts_in = os.environ["PATH_SCRIPTS_IN"]

prepared_mark = os.path.join(path_build_root, ".prepared")

if not os.path.exists(prepared_mark):
    logger.info("Start preparing build root")
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config.get('UrlConfig', 'arch_aarch64_rootfs_url')
    download_to_dir(url, path_build_resources, 'aarch64_rootfs.tar.gz')
    try:
        extract_to_dir(f"sudo bsdtar -C {path_build_root} --acls --xattrs -xpf "
                       + os.path.join(path_build_resources, "aarch64_rootfs.tar.gz"), path_build_root)
        mirror_url = url = config.get('PacManConfig', 'mirror_url')
        if mirror_url:
            mirrorlist_path = os.path.join(
                path_build_root, "etc/pacman.d/mirrorlist")
            with open(mirrorlist_path, 'r') as rfile:
                file_data = rfile.read()
                old_url = 'http://mirror.archlinuxarm.org/$arch/$repo'
                new_file_data = file_data.replace(old_url, mirror_url)
                with open(mirrorlist_path, 'w') as wfile:
                    wfile.write(new_file_data)
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
