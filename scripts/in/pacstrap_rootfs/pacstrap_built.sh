relative_source ../shell_log.sh

pacstrap_built() {
  log_i "Pacstrapping built packages into ${dir_pacstrap_rootfs}..."
  if compgen "${dir_pkg_built}/*" >/dev/null; then
    sudo pacstrap -U "${dir_pacstrap_rootfs}" "${dir_pkg_built}/"*
  else
    log_i "No built packages found"
  fi
  log_i "Pacstrap built packages done"
}
