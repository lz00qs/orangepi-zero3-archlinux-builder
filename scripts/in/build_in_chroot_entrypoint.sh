#!/bin/bash -e

cd /home/alarm/build/
export HOME=/home/alarm

sudo --preserve-env=GOPROXY,http_proxy,https_proxy,build_option -u alarm ./build.sh