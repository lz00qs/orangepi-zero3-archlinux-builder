relative_source shell_log.sh
relative_source pacstrap_rootfs/pacstrap_from_repo.sh
relative_source pacstrap_rootfs/pacstrap_built.sh
relative_source configure_rootfs.sh

pacstrap_rootfs() {
    sudo mkdir -p "${dir_pacstrap_rootfs}"
    sudo chown root:root "${dir_pacstrap_rootfs}"
    sudo mount -o bind "${dir_pacstrap_rootfs}" "${dir_pacstrap_rootfs}"
    pacstrap_from_repo
    pacstrap_built
    configure_rootfs
    sudo umount -l -r "${dir_pacstrap_rootfs}"
}