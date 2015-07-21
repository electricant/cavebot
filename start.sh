#!/bin/bash
#
# Launch cavebot as the user 'nobody'
# To run chrooted the following commands are needed:
#	mount -o bind /dev /chroot-dir/dev
#	mount -o bind /dev/pts /chroot-dir/dev

# setup locales
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export PYTHONIOENCODING=utf-8

cd /srv/cavebot/
su nobody --shell=/bin/sh -c "python3 CaveBot.py"
