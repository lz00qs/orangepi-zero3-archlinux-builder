source ../shell_log.sh

should_build() {
    local dir_pkg=$1
    local dir_pkg_built=$2 # absolute path
    if [ -d $dir_pkg ]; then
        pushd $dir_pkg
        . PKGBUILD
        for i in "${pkgname[@]}"; do
            pkgfilename="${i}-${pkgver}-${pkgrel}-aarch64.pkg.tar"
            pkgfile="${dir_pkg_built}/${pkgfilename}"
            if [ ! -f $pkgfile ]; then
                log_i "${pkgfilename} not found, should build $dir_pkg"
                return 0
            fi
        done
        popd >/dev/null
        log_i "Package $dir_pkg already built"
    else
        log_error "Package $dir_pkg not found"
        return 1
    fi
    return $?
}
