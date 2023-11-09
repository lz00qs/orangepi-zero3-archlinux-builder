import configparser
import os
import shutil
import subprocess
import sys
from scripts.out.py_modules.tools import Logger, run_cmd_with_exit
logger = Logger(name="log")


# def get_config(path_config, config_name):
#     config_str = ''
#     with open(path_config, 'r') as input_file:
#         lines = input_file.readlines()
#         in_url_config = False  # 标志，指示是否在 UrlConfig 部分
#         for line in lines:
#             line = line.strip()  # 去除首尾空格和换行符
#             if line == f'[{config_name}]':
#                 in_url_config = True  # 进入 UrlConfig 部分
#             elif line.startswith('[') and in_url_config:
#                 in_url_config = False  # 退出 UrlConfig 部分
#             elif in_url_config and '=' in line:
#                 key, value = line.split('=', 1)
#                 config_str = config_str + f'{key.strip()}={value.strip()}\n'
#     return config_str.rstrip('\n')


# distccd_pid = ''
# def start_distcc():
#     logger.info("Starting distcc...")
#     try:
#         distccd_pid_file = subprocess.run("mktemp", shell=True, check=True, capture_output=True).stdout.decode('utf-8').rstrip('\n')
#         path_build_toolchains = os.environ["PATH_BUILD_TOOLCHAINS"]
#         new_path_entry = f"{path_build_toolchains}/xtools/aarch64-unknown-linux-gnu/bin"
#         current_path = os.environ.get('PATH', '')
#         if new_path_entry not in current_path:
#             new_path = f'{new_path_entry}:{current_path}'
#             os.environ['PATH'] = new_path
#         run_cmd_with_exit(f"distccd --daemon --allow-private --make-me-a-botnet --pid-file {distccd_pid_file} --log-file /home/whale/orangepi-zero3-archlinux-build/distcc.log --verbose")
#         global distccd_pid
#         distccd_pid = subprocess.run(f"sudo cat {distccd_pid_file}", shell=True, check=True, capture_output=True).stdout.decode('utf-8').rstrip('\n')
#         logger.debug(f"distccd pid: {distccd_pid}")
#     except Exception as e:
#         logger.error("Create temp file error. " + e.__str__())
#         sys.exit(1)
#     finally:
#         try:
#             logger.info(f"Removing temp file: {distccd_pid_file}")
#             run_cmd_with_exit(f"sudo rm -f {distccd_pid_file}")
#         except Exception as e:
#             logger.error("Remove temp file error. " + e.__str__())
#             sys.exit(1)

# def stop_distcc():
#     logger.info("Stopping distcc...")
#     try:
#         run_cmd_with_exit(f"sudo kill {distccd_pid}")
#     except Exception as e:
#         logger.error("Kill distccd error. " + e.__str__())
#         sys.exit(1)

# toolchain_list = ["c++", "cc", "cpp", "g++", "gcc"]
# original_toolchain_links_paths = {}
# def link_toolchains():
#     for toolchain in toolchain_list:
#         symbolic_link = shutil.which(toolchain)
#         if symbolic_link:
#             src = os.readlink(symbolic_link)
#             if src:
#                 global original_toolchain_links_paths
#                 original_toolchain_links_paths[symbolic_link] = src
#                 logger.debug(f"Original link: {toolchain} -> " + src)
#             os.system(f"sudo rm {symbolic_link}")
#         path_build_toolchains_xtools = os.environ["PATH_BUILD_TOOLCHAINS_XTOOLS"]
#         cross_bin = f"{path_build_toolchains_xtools}/aarch64-unknown-linux-gnu/bin/aarch64-unknown-linux-gnu-"
#         os.system(f"sudo ln -s {cross_bin}{toolchain} {symbolic_link}")
#     for toolchain in toolchain_list:
#         os.system(f"{toolchain} --version")

# def unlink_toolchains():
#     for symbolic_link in original_toolchain_links_paths:
#         os.system(f"sudo rm {symbolic_link}")
#         os.system(f"sudo ln -s {original_toolchain_links_paths[symbolic_link]} {symbolic_link}")


def build_in_chroot():
    logger.info("Start building in chroot")
    path_build_in_root = '/home/alarm/build'
    path_build_root = os.environ["PATH_BUILD_ROOT"]
    path_build_in_root_absolute = f"{path_build_root}{path_build_in_root}"
    path_scripts_in = os.environ["PATH_SCRIPTS_IN"]
    path_base = os.environ["PATH_BASE"]
    try:
        logger.info("Copying files into build_root...")
        run_cmd_with_exit(f"sudo mkdir -p {path_build_in_root_absolute}")
        run_cmd_with_exit(
            f"sudo cp -ra {path_scripts_in}/* {path_build_in_root_absolute}/")
        run_cmd_with_exit(
            f"sudo cp -ra {path_base}/pkg {path_build_in_root_absolute}/")
        if os.environ["CROSS"]:
            run_cmd_with_exit(
                f"sudo cp -ra {path_base}/pkg_cross {path_build_in_root_absolute}/")
        run_cmd_with_exit(
            f"sudo cp -ra {path_base}/pkg_built {path_build_in_root_absolute}/")
        # run_cmd_with_exit(
        #     f"sudo cp -ra {path_base}/releases {path_build_in_root_absolute}/")
        run_cmd_with_exit(
            f"sudo cp -ra {path_base}/booting {path_build_in_root_absolute}/")
        run_cmd_with_exit(
            f"sudo cp -ra {path_base}/scripts/shell_log.sh {path_build_in_root_absolute}/")
        run_cmd_with_exit(
            f"sudo cp -ra {path_base}/scripts/should_build.sh {path_build_in_root_absolute}/")
        config = os.environ["PATH_CONFIG_IN"]
        run_cmd_with_exit(f"sudo cp -ra {config} {path_build_in_root_absolute}/config")
        logger.info("Mounting filesystems...")
        run_cmd_with_exit(
            f"sudo mount -o bind {path_build_root} {path_build_root}")
        logger.info("Getting inside chroot...")
        run_cmd_with_exit(
            f"sudo --preserve-env=GOPROXY,http_proxy,https_proxy arch-chroot {path_build_root} {path_build_in_root}/build_in_chroot_entrypoint.sh")
        original_directory = os.getcwd()
        os.chdir(path_base)
        for copy_back_folder in ["pkg_built"]:
            if subprocess.run(f"sudo tar -C {path_build_in_root_absolute} -c {copy_back_folder} | tar -x {copy_back_folder}", shell=True, check=True).returncode == 0:
                subprocess.run(
                    f"sudo chown -R $(id --user):$(id --group) {copy_back_folder}", shell=True, check=True)
        
        path_pacstrap_rootfs = os.environ["PATH_PACSTRAP_ROOTFS"]
        release_prefix = os.environ["RELEASE_PREFIX"]
        os.chdir(path_pacstrap_rootfs)
        run_cmd_with_exit(f"sudo bsdtar --acls --xattrs -cpf -  * | pigz -c -p32 > {path_base}/releases/{release_prefix}-rootfs.tar.gz")
        
        os.chdir(original_directory)
    except Exception as e:
        logger.error("Extract build root error. " + e.__str__())
        sys.exit(1)
    finally:
        try:
            os.chdir(original_directory)
        except Exception as e:
            logger.error("Change directory error. " + e.__str__())
        try:
            logger.info("Unmounting filesystems...")
            run_cmd_with_exit(f"sudo umount -l -R {path_build_root}")
            logger.info("Removing files from build_root...")
            run_cmd_with_exit(f"sudo rm -rf {path_build_in_root_absolute}")
        except Exception as e:
            logger.error(f"Build in chroot finally excution error. " + e)
            sys.exit(1)
        logger.info("do something finally...")
