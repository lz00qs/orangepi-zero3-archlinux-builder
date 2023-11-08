#!/bin/bash
pacman -Rcns linux-aarch64 vi --noconfirm
pacman-key --init
pacman-key --populate
pacman -Syu --noconfirm \
  arch-install-scripts \
  base-devel \
  distcc \
  dosfstools \
  git \
  go \
  parted \
  sudo \
  uboot-tools \
  wget \
  xz \
  python
echo 'alarm ALL=(ALL:ALL) NOPASSWD: ALL' >/etc/sudoers.d/alarm_allow_sudo_no_passwd
# sed  "s/(!distcc/(distcc/g
#       s/#DISTCC_HOSTS=\"\"/DISTCC_HOSTS=127.0.0.1/g
#       s/#MAKEFLAGS=\"-j2\"/MAKEFLAGS=\"-j$(($(nproc) * 2))\"/g" -i /etc/makepkg.conf
