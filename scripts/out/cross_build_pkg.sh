#!/bin/bash -e

source ../shell_log.sh
source ../should_build.sh

log_i "Cross building packages..."

if [[ -d "${PATH_PKG_CROSS}" ]]; then
    cross_prefix=${PATH_BUILD_TOOLCHAINS_XTOOLS}/aarch64-unknown-linux-gnu/bin/aarch64-unknown-linux-gnu-
    pushd "${PATH_PKG_CROSS}" >/dev/null
    for build_pkg in *; do
        if [[ -d "${build_pkg}" ]]; then
            dir_build_pkg="${PATH_PKG}/${build_pkg}"
            if [[ -d "${dir_build_pkg}" ]]; then
                pushd "${dir_build_pkg}" >/dev/null
                if should_build "${build_pkg}" "${PATH_PKG_BUILT}"; then
                    should_build_pkg='yes'
                else
                    hould_build_pkg=''
                fi
                popd >/dev/null
                if [[ "${should_build_pkg}" ]]; then
                    pushd "${build_pkg}" >/dev/null
                    (
                        threads=$(($(nproc) + 1))
                        export ARCH=arm64
                        export CROSS_COMPILE="${cross_prefix}"
                        export MAKEFLAGS="${MAKEFLAGS} ARCH=${ARCH} CROSS_COMPILE=${CROSS_COMPILE} -j${threads}"
                        . build.sh
                    )
                    popd >/dev/null
                fi
            else
                log_w "Ignored cross package ${build_pkg} since we did no find its generic counterpart under ${dir_build_pkg}"
            fi
        fi
    done
    popd >/dev/null
fi

log_i "Cross building packages success"
