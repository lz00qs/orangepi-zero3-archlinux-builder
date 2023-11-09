#!/bin/bash -e

source ../shell_log.sh
source ../should_build.sh

log_i "Downloading packages..."
LIBRARY="${PATH_BUILD_ROOT}/usr/share/makepkg"
MAKEPKG_CONF="${PATH_BUILD_ROOT}/etc/makepkg.conf"
SRCDEST=.
lib=
(
    for lib in "$LIBRARY"/*.sh; do
        source "$lib"
    done
    load_makepkg_config
    pushd "${PATH_PKG}" >/dev/null
    for build_pkg in *; do
        if [[ -d "${build_pkg}" ]]; then
            pushd "${build_pkg}" >/dev/null
            if should_build "${build_pkg}" "${PATH_PKG_BUILT}"; then
                log_i "Downloading ${build_pkg}..."
                if (
                    source_safe PKGBUILD
                    download_sources novcs allarch
                ); then
                    log_i "Download ${build_pkg} success"
                else
                    log_e "Download ${build_pkg} failed"
                    exit 1
                fi
            fi
            popd >/dev/null
        fi
    done
    popd >/dev/null
    log_i "Download packages success"
)
