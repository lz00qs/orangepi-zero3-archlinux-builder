
import os
import subprocess
import sys
import logging


# Usage:
# from logsys.logger import Logger
# logger = Logger(name="log")
# logger.info("info")
# logger.error("error")
# logger.warning("waring")
# logger.critical("critical")
# logger.debug("debug")


log_colors_config = {
    'DEBUG': 'bold_cyan',
    'INFO': 'bold_green',
    'WARNING': 'bold_yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'red',
}


class Logger(logging.Logger):
    def __init__(self, name, level='DEBUG', file=None, encoding='utf-8'):
        super().__init__(name)
        global_log_level = os.getenv('global_log_level', 'DEBUG').upper()
        log_level = logging.DEBUG
        if global_log_level == 'INFO':
            log_level = logging.INFO
        elif global_log_level == 'WARNING':
            log_level = logging.WARNING
        elif global_log_level == 'ERROR':
            log_level = logging.ERROR
        elif global_log_level == 'CRITICAL':
            log_level = logging.CRITICAL
        try:
            import colorlog
        except ImportError:
            print("colorlog not installed. Installing...")
            try:
                subprocess.run(['pip3', 'install', 'colorlog'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print("colorlog installed.")
                import colorlog
            except subprocess.CalledProcessError:
                print("colorlog install failed.")
                sys.exit(1)
        self.encoding = encoding
        self.file = file
        self.level = level
        formatter = colorlog.ColoredFormatter(
            # '%(log_color)s%(asctime)s [%(filename)s:%(''lineno)d] %(log_color)s[%(levelname)s] %(message)s',
            '%(log_color)s%(asctime)s %(log_color)s[%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors=log_colors_config,
            secondary_log_colors={
                'message': {
                    'DEBUG': 'blue',
                    'INFO': 'blue',
                    'WARNING': 'blue',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red'
                }
            },
            style='%'
        )
        console = colorlog.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(formatter)
        self.addHandler(console)
        self.setLevel(log_level)


logger = Logger(name="log")


def clone_to_dir(url, dir, branch=None):
    def clone():
        try:
            return_code = subprocess.run(
                f"git clone {url} {dir}", shell=True, check=True).returncode
            if return_code != 0:
                logger.error(f"Clone {url} failed.")
                sys.exit(1)

            if branch:
                return_code = subprocess.run(
                    f"git -C {dir} checkout {branch}", shell=True, check=True).returncode
                if return_code != 0:
                    logger.error(f"Checkout {branch} failed.")
                    sys.exit(1)

            return_code = subprocess.run(
                "touch " + os.path.join(dir, ".clone_finished"), shell=True, check=True).returncode
            if return_code != 0:
                logger.error(
                    f"Touch {os.path.join(dir,'.clone_finished')} failed.")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Clone {url} failed.")
            sys.exit(1)
    if not os.path.exists(dir):
        clone()
    else:
        if not os.path.exists(os.path.join(dir, ".clone_finished")):
            try:
                return_code = subprocess.run(
                    f"sudo rm -rf {dir}", shell=True, check=True).returncode
                if return_code != 0:
                    logger.error(f"Remove {dir} failed.")
                    sys.exit(1)
                clone()
            except Exception as e:
                logger.error(f"Pull {url} failed.")
                sys.exit(1)
        else:
            logger.info(f"{url} already exists. Using existing files.")
            # logger.info(f"{url} already exists.")
            # try:
            #     return_code = subprocess.run(f"git -C {dir} pull --force", shell=True, check=True).returncode
            #     if return_code != 0:
            #         logger.error(f"Pull {url} failed.")
            #         sys.exit(1)
            # except Exception as e:
            #     logger.error(f"Pull {url} failed.")
            #     sys.exit(1)


def download_to_dir(url, dir, file_name=None):
    cmd = ''
    if file_name:
        cmd = f"wget {url} -P {dir} -O {dir}/{file_name}"
    else:
        cmd = f"wget {url} -P {dir}"
        file_name = os.path.basename(url)
    finished_file_name = f".{file_name}_download_finished"

    def download():
        try:
            return_code = subprocess.run(
                cmd, shell=True, check=True).returncode
            if return_code != 0:
                logger.error(f"Download {url} failed.")
                sys.exit(1)
            return_code = subprocess.run(
                "touch " + os.path.join(dir, finished_file_name), shell=True, check=True).returncode
            if return_code != 0:
                logger.error(f"Touch {finished_file_name} failed.")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Download {url} failed.")
            sys.exit(1)

    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
        download()
    else:
        if not os.path.exists(os.path.join(dir, finished_file_name)):
            try:
                subprocess.run(
                    f"sudo rm -rf {os.path.join(dir, file_name)}", shell=True, check=True)
                download()
            except Exception as e:
                logger.error(f"Download {url} failed.")
                sys.exit(1)
        else:
            logger.info(f"{url} already exists. Using existing files.")


def extract_to_dir(extract_cmd, dir):
    def extract():
        try:
            return_code = subprocess.run(
                extract_cmd, shell=True, check=True).returncode
            if return_code != 0:
                logger.error(f"{extract_cmd} failed.")
                sys.exit(1)
            return_code = subprocess.run(
                "touch " + os.path.join(dir, ".extract_finished"), shell=True, check=True).returncode
            if return_code != 0:
                logger.error(
                    f"Touch {os.path.join(dir, '.extract_finished')} failed.")
                sys.exit(1)
        except Exception as e:
            logger.error(f"{extract_cmd} failed.")
            sys.exit(1)

    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
        extract()
    else:
        if not os.path.exists(os.path.join(dir, ".extract_finished")):
            try:
                return_code = subprocess.run(
                    f"sudo rm -rf {dir}", shell=True, check=True).returncode
                if return_code != 0:
                    logger.error(f"Remove {dir} failed.")
                    sys.exit(1)
                os.makedirs(dir, exist_ok=True)
                extract()
            except Exception as e:
                logger.error(f"{extract_cmd} failed.")
                sys.exit(1)
        else:
            logger.info(f"{dir} already extracted. Using existing files.")


def run_relative_shell(shell_path, sudo=False):
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.dirname(shell_path))
        if sudo:
            return_code = subprocess.run(
                f"sudo -E bash {os.path.basename(shell_path)}", shell=True, check=True).returncode
        else:
            return_code = subprocess.run(
                f"bash {os.path.basename(shell_path)}", shell=True, check=True).returncode
        if return_code != 0:
            logger.error(f"{shell_path} failed.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"{shell_path} failed.")
        sys.exit(1)
    finally:
        os.chdir(current_dir)


def run_cmd_with_exit(cmd, exit_code=1):
    try:
        return_code = os.system(cmd)
        if return_code != 0:
            logger.error(f"{cmd} failed.")
            sys.exit(exit_code)
    except Exception as e:
        logger.error(f"{cmd} failed.")
        sys.exit(exit_code)
        
def prepare_config(config_path):
    with open(config_path, 'r') as original_file:
        original_contents = original_file.read()
    # with open(f"{config_path}.bak", 'w') as backup_file:
    #     backup_file.write(original_contents)
    start_pos = original_contents.find('[BuildConfig]')
    if start_pos == -1:
        logger.error("[BuildConfig] section not found in the original file.")
        exit(1)
    end_pos = original_contents.find('[', start_pos + 1)
    if end_pos == -1:
        end_pos = len(original_contents)
    build_config_contents = original_contents[start_pos:end_pos]
    config_in = subprocess.run("mktemp", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    os.environ["PATH_CONFIG_IN"] = config_in
    with open(config_in, 'w') as new_file:
        new_file.write(build_config_contents.replace('[BuildConfig]', '').strip())
    split_contents = original_contents[:start_pos] + original_contents[end_pos:]
    with open(f"{config_path}.split", 'w') as split_file:
        split_file.write(split_contents)

def restore_config(config_path):
    # os.system(f"mv {config_path}.bak {config_path}")
    os.system("rm -f " + f"{config_path}.split")
    
