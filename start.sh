#!/bin/bash
#
# Launch cavebot as the user 'nobody'
# To run chrooted the following commands are needed:
#	mount -o bind /dev /chroot-dir/dev
#	mount -o bind /dev/pts /chroot-dir/dev

cd /srv/cavebot/
su nobody -c "python3 CaveBot.py"
