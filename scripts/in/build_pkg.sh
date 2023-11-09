relative_source shell_log.sh
relative_source should_build.sh

move_built_to_pkg() {
    local build_pkg="$1"
    local dir_pkg_absolute="$2"
    (
        . PKGBUILD
        if [[ ${arch[0]} == 'any' ]]; then
            local arch_naming='any'
        else
            local arch_naming='aarch64'
        fi
        for i in "${pkgname[@]}"; do
            if [[ $(type -t pkgver) == 'function' ]]; then
                pkgfile_glob1="${i}-"
                pkgfile_glob2="-${pkgrel}-${arch_naming}${PKGEXT}"
                chmod -x "${pkgfile_glob1}"*"${pkgfile_glob2}"
                mv -vf "${pkgfile_glob1}"*"${pkgfile_glob2}" "${dir_pkg_absolute}/"
            else
                pkgfile="${i}-${pkgver}-${pkgrel}-${arch_naming}${PKGEXT}"
                chmod -x "${pkgfile}"
                mv -vf "${pkgfile}" "${dir_pkg_absolute}/"
            fi
        done
    )
}

build_pkg() {
    log_i "Starting build pkg..."
    log_i "Cleaning build dir..."
    find "${dir_pkg}" -maxdepth 2 -name '*-aarch64.pkg.tar' -exec rm -rf {} \;
    mkdir -p "${dir_pkg_built}"
    if compgen -G "${dir_pkg_built}/"* &>/dev/null && ! chmod u+x "${dir_pkg_built}/"*; then
        log_i "Failed to mark all existing package files are executable to use as check flag"
        exit 1
    fi
    local dir_pkg_absolute=$(readlink -f "${dir_pkg}")
    local dir_pkg_cross_absolute=$(readlink -f "${dir_pkg_cross}")
    local dir_pkg_built_absolute=$(readlink -f "${dir_pkg_built}")
    local PKGEXT=.pkg.tar
    export PKGEXT
    # if should_build "${dir_pkg_absolute}/${build_pkg}" "${dir_pkg_built_absolute}"; then
    pushd "${dir_pkg}" >/dev/null
    for build_pkg in *; do
        if [[ ! -d "${build_pkg}" ]]; then
            continue
        fi
        pushd "${build_pkg}" >/dev/null
        if should_build "${build_pkg}" "${dir_pkg_built_absolute}"; then
            log_i "Building package ${build_pkg}..."
            if [[ -d "${dir_pkg_cross_absolute}" ]]; then
                local dir_build_cross_pkg="${dir_pkg_cross_absolute}/${build_pkg}"
                if [[ -d "${dir_build_cross_pkg}" ]]; then
                    cross_guest_pkg='yes'
                    log_i "Cross build replacement for ${build_pkg} found, use ${dir_build_cross_pkg} instead"
                    pushd "${dir_build_cross_pkg}" >/dev/null
                else
                    cross_guest_pkg=''
                fi
            fi
            local retry=3
            local success=''
            while [[ ${retry} -ge 0 ]]; do
                makepkg -cfsAC --noconfirm
                if [[ $? == 0 ]]; then
                    success='yes'
                    break
                fi
                log_w "Retrying to build package ${build_pkg}, retries left: ${retry}"
            done
            if [[ -d "${dir_pkg_cross_absolute}" && "${cross_guest_pkg}" ]]; then
                popd >/dev/null
                cp "${dir_build_cross_pkg}/"*'.pkg.tar' .
            fi
            if [[ -z "${success}" ]]; then
                log_e "Failed to build package ${build_pkg} after 3 retries"
                exit 1
            fi
            move_built_to_pkg "${build_pkg}" "${dir_pkg_built_absolute}"
        fi
        popd >/dev/null
    done
    popd >/dev/null
    local i
    for i in "${dir_pkg_built}/"*; do
        if [[ -x "${i}" ]]; then
            rm -f "${i}"
        fi
    done
    log_i "Packages built"
}
