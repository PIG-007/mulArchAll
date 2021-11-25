#! /usr/bin/env bash


apt-get -y install gcc-mips-linux-gnu
apt-get -y install g++-mips-linux-gnu
apt-get -y install pkg-config-mips-linux-gnu

apt-get -y install gcc-mipsel-linux-gnu
apt-get -y install g++-mipsel-linux-gnu
apt-get -y install pkg-config-mipsel-linux-gnu

apt-get -y install gcc-mips64el-linux-gnuabi64
apt-get -y install g++-mips64el-linux-gnuabi64
apt-get -y install pkg-config-mips64el-linux-gnuabi64

apt-get -y install gcc-mips64-linux-gnuabi64
apt-get -y install g++-mips64-linux-gnuabi64
apt-get -y install pkg-config-mips64-linux-gnuabi64

apt-get -y install gcc-arm-linux-gnueabi
apt-get -y install g++-arm-linux-gnueabi
apt-get -y install pkg-config-arm-linux-gnueabi

apt-get -y install gcc-arm-linux-gnueabihf
apt-get -y install g++-arm-linux-gnueabihf
apt-get -y install pkg-config-arm-linux-gnueabihf

apt-get -y install gcc-aarch64-linux-gnu
apt-get -y install g++-aarch64-linux-gnu
apt-get -y install pkg-config-aarch64-linux-gnu

apt-get -y install wget
apt-get -y install gcc
apt-get -y install make
apt-get -y install build-essential bison
apt-get -y install libgdbm-dev libc6-dev gawk
apt-get -y install qemu
apt-get -y install gdb-multiarch
apt-get -y install gdbserver

chmod a+x ~/mulArchAll/CMD/*
cp ~/mulArchAll/CMD/* /usr/bin/
cp ~/mulArchAll/gdbinit/gdbinitPwndbg ~/.gdbinit