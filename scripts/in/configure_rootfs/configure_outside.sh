relative_source ../shell_log.sh

configure_outside() {
    log_i "Configuring basic setup outside the target rootfs..."

    if [[ -z "${mirror_url}" ]]; then
        log_i "No mirror URL is set, skipping setting up pacman mirrorlist"
    else
        log_i "Setting up pacman mirrorlist"
        local orig_mirrorlist_path="${dir_pacstrap_rootfs}/etc/pacman.d/mirrorlist"
        local orig_mirror_url="http://mirror.archlinuxarm.org/\$arch/\$repo"
        local sed_cmd="s#${orig_mirror_url}#${mirror_url}#g"
        sudo sed -i $sed_cmd $orig_mirrorlist_path
    fi

    log_i "Setting timezone to ${timezone}"
    sudo ln -sf "/usr/share/zoneinfo/${timezone}" "${dir_pacstrap_rootfs}/etc/localtime"
    local locale_enable=()
    local locale_subst=''
    local locale_report=''
    local started=''
    for locale_enable in "${locales_enable[@]}"; do
        locale_subst+="s|^#${locale_enable}  $|${locale_enable}  |g
        "
        if [[ "${started}" ]]; then
            locale_report+=", '${locale_enable}'"
        else
            locale_report+="'${locale_enable}'"
        fi
        started='yes'
    done
    log_i "Enabling locales: ${locale_report}"
    sudo sed -i "${locale_subst}" "${dir_pacstrap_rootfs}/etc/locale.gen"
    log_i "Setting '${locale_use}' as locale"
    echo "LANG=${locale_use}" | sudo tee "${dir_pacstrap_rootfs}/etc/locale.conf"
    log_i "Setting hostname to '${hostname}'"
    echo "${hostname}" | sudo tee "${dir_pacstrap_rootfs}/etc/hostname"
    log_i "Setting basic localhost"
    printf '127.0.0.1\tlocalhost\n::1\t\tlocalhost\n' | sudo tee -a "${dir_pacstrap_rootfs}/etc/hosts"
    log_i "Setting DHCP on eth* and en* with systemd-networkd"
    printf '[Match]\nName=eth* en*\n\n[Network]\nDHCP=yes\nDNSSEC=no\n' | sudo tee "${dir_pacstrap_rootfs}/etc/systemd/network/20-wired.network"
    log_i "Creating symbol link /etc/resolve.conf => /run/systemd/resolve/resolv.conf in case systemd-resolved fails to set it up"
    sudo ln -sf /run/systemd/resolve/resolv.conf "${dir_pacstrap_rootfs}/etc/resolv.conf"
    if [[ "${link_vi_to_vim}" == 'yes' ]]; then
        log_i "Setting VIM as VI..."
        sudo ln -sf 'vim' "${dir_pacstrap_rootfs}/usr/bin/vi"
    fi
    if [[ "${sudo_allow_wheel}" == 'yes' ]]; then
        log_i "Setting up sudo, to allow users in group wheel to use sudo with password"
        local sudoers="${dir_pacstrap_rootfs}/etc/sudoers"
        sudo chmod o+w "${sudoers}"
        sudo sed -i 's|^# %wheel ALL=(ALL:ALL) ALL$|%wheel ALL=(ALL:ALL) ALL|g' "${sudoers}"
        sudo chmod o-w "${sudoers}"
    fi
    if [[ "${ssh_root_with_password}" == 'yes' ]]; then
        log_i 'Setting up SSH, to allow to login as root with password'
        sudo sed -i 's|^#PermitRootLogin prohibit-password$|PermitRootLogin yes|g' "${dir_pacstrap_rootfs}/etc/ssh/sshd_config"
    fi
    local pacman_mirrorlist_pkg=$(ls "${dir_pacstrap_rootfs}/var/cache/pacman/pkg/pacman-mirrorlist-"*'.pkg.tar'* | grep -v '.sig$' | tail -n 1)
    if [[ "${pacman_mirrorlist_pkg}" ]]; then
        log_i "Setting pacman mirror to geo-IP based global mirror"
        tar -xOf "${pacman_mirrorlist_pkg}" 'etc/pacman.d/mirrorlist' |
            sed 's_#\(Server = .*geo.*$\)_\1_' |
            sudo tee "${dir_pacstrap_rootfs}/etc/pacman.d/mirrorlist" >/dev/null
    fi
    log_i "Completed basic setup outside the target root"
}
