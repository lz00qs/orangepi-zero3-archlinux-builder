import os
from tools import extract_to_dir

path_build_resources = os.environ["PATH_BUILD_RESOURCES"]
path_build_root = os.environ["PATH_BUILD_ROOT"]

extract_to_dir(f"sudo bsdtar -C {path_build_root} --acls --xattrs -xpf "
               + os.path.join(path_build_resources, "aarch64_rootfs.tar.gz"), path_build_root)
