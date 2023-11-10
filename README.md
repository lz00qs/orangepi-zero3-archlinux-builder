# Orange Pi Zero3 Arch Linux ARM Image Builder

This repository is dedicated to building an Arch Linux ARM image for the Orange Pi Zero3.

## Acknowledgments

Thanks to `https://github.com/7Ji/orangepi5-archlinuxarm`. Their work and project served as a valuable reference and inspiration for this repository.

If you have any problem, please open an issue.

Also, welcome to contribute this repo to make this repo better!

## Usage

This builder has only been verified on debian > 10 and ubuntu > 20.04.


Firstly, install the required build package in your system:
```bash
sudo apt install \
   arch-install-scripts \
   bc \
   bison \
   distcc \
   flex \
   libarchive-tools \
   qemu-user-static \
   libssl-dev \
   qemu-user-static \
   u-boot-tools \
   python \
   python3-pip
```


Secondly, clone this repo with `--recursive` option:
```bash
git clone --recursive https://github.com/lz00qs/orangepi-zero3-archlinux-builder.git
```


Finally, build:
```bash
python3 build.py
```
You can also set the build option to pkg, rootfs, img to choose what you want to build:
```bash
python3 build.py --build img
```
> Default value is img, that means you will get an image finally.

> You can change some configurations in `config.ini`.

You can use clean.py to clean all built files:
```bash
python3 clean.py
```

## Contributions

@lz00qs

## License

GPL V3.0