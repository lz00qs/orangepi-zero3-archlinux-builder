should_build() {
  local dir_pkg_built_absolute=$2
  local build_pkg=$1
  (
    . PKGBUILD
    pkgfiles=()
    for i in "${pkgname[@]}"; do
      pkgfilename="${i}-${pkgver}-${pkgrel}-aarch64${PKGEXT}"
      pkgfile="${dir_pkg_built_absolute}/${pkgfilename}"
      if [[ -f "${pkgfile}" ]]; then
        pkgfiles+=("${pkgfile}")
      else
        log_i "${pkgfilename} provided by ${1} not found in built packages, should build ${1}"
        exit 0
      fi
    done
    for pkgfile in "${pkgfiles[@]}"; do
      chmod -x "${pkgfile}"
    done
    log_i "All package files existing for ${1}, can be skipped"
    exit 1
  )
  return $?
}
