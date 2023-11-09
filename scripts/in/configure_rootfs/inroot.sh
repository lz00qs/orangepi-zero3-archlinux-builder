basic_setup() {
  echo " => Basic setup inside the target root"
  echo "  -> Generating locales..."
  locale-gen
  if [[ ${#enable_systemd_units[@]} == 0 ]]; then
    return
  fi
  echo "  -> Enabling systemd units: ${enable_systemd_units[@]}"
  systemctl enable "${enable_systemd_units[@]}"
}

setup_users() {
  echo " => Setting up users"
  if [[ "${root_password}" ]]; then
    echo "  -> Setting root's password to ${root_password}"
    printf '%s\n%s\n' "${root_password}" "${root_password}" | passwd
  else
    echo "  -> Warning: root's password is not set, you will not be able to login as root!"
  fi
  local create_user
  local userinfo=()
  for create_user in "${create_users[@]}"; do
    echo "  -> Parsing user definition: '${create_user}'"
    userinfo=($(sed 's/\(.*\)@\(.*\):\(.*\)/\1\n\2\n\3/' <<<"${create_user}"))
    if [[ -z "${userinfo[0]}" ]]; then
      echo "   -> Failed to get username"
      return 1
    fi
    echo "   -> Username: ${userinfo[0]}"
    if [[ -z "${userinfo[1]}" ]]; then
      useradd -m ${userinfo[0]}
    else
      echo "   -> Group: ${userinfo[1]}"
      useradd -g ${userinfo[1]} -m ${userinfo[0]}
    fi
    if [[ "${userinfo[2]}" ]]; then
      echo "   -> Password: ${userinfo[2]}"
      printf '%s\n%s\n' "${userinfo[2]}" "${userinfo[2]}" | passwd "${userinfo[0]}"
    else
      echo "   -> Warning: no password is set, you will not be able to login as this user"
    fi
  done
}

inside_root() {
  basic_setup
  setup_users
}

inside_root
