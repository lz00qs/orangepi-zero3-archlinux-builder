relative_source configure_rootfs/configure_outside.sh
relative_source configure_rootfs/configure_inside.sh

configure_rootfs() {
    log_i "Configuring basic setup outside the target rootfs..."
    configure_outside
    log_i "Completed basic setup outside the target root"
    log_i "Configuring basic setup inside the target rootfs..."
    configure_inside
    log_i "Completed basic setup inside the target root"
}
