#!/bin/bash

cd ~
mkdir ~/device_trees/
cd ~/device_trees/

cp /boot/efi/dtb/qcom/qrb2210-ardiuno-imola-camera-rpiv2.dtb ~/device_trees/

fdtoverlay -i qrb2210-arduino-imola-camera-rpiv2.dtb unoq-imx219-powerfix.dtbo -o qrb2210-arduino-imola-camera-rpiv2-r1b.dtb

mkdir /boot/efi/dtb/r1b/
cp qrb2210-arduino-imola-camera-rpiv2-r1b.dtb /boot/efi/dtb/r1b/

