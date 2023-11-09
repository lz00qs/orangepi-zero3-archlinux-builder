relative_source ../shell_log.sh

pacstrap_from_repo() {
  if [[ "${#pacstrap_from_repo_pkgs[@]}" == 0 ]]; then
    return
  fi
  log_i "Pacstrapping following packages from repo into ${dir_pacstrap_rootfs}..."
  local pkg_line pkg_names=()
  for pkg_line in "${pacstrap_from_repo_pkgs[@]}"; do
    log_i "${pkg_line}"
    pkg_names+=("${pkg_line%%:*}")
  done
  sudo pacstrap "${dir_pacstrap_rootfs}" "${pkg_names[@]}"
  log_i "Pacstrap base done"
}
