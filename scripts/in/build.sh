#!/bin/bash -e

. relative_source.sh
relative_source config
relative_source shell_log.sh
relative_source build_pkg.sh
relative_source pacstrap_rootfs.sh

build_pkg
pacstrap_rootfs