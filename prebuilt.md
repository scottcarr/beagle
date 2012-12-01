#Using the latest Wind Project pre-built image

We need a way of formating the SD card in the right way.  I haven't found
a good way of doing that yet.  So, for now, lets just use one of the demo
images and overwrite it.

You need at least a 4GB SD card for this method. 

##Setup SD card partitions with a demo image

Skip this step if you've already got a correctly formatted SD card.

Put your SD card in your computer and figure out what letter it is (like /dev/sdX)
where X might be b

Run:

    $ wget http://downloads.angstrom-distribution.org/demo/beaglebone/Angstrom-Cloud9-IDE-GNOME-eglibc-ipk-v2012.05-beaglebone-2012.09.12.img.xz
    $ sudo -s
      (type in your password)
    # xz -dkc Angstrom-Cloud9-IDE-GNOME-eglibc-ipk-v2012.05-beaglebone-2012.09.12.img.xz > /dev/sdX
    # exit

##Deploy the image
That should make 2 partitions on your SD card, mount them:

    sudo mkdir /mnt/rootfs
    sudo mkdir /mnt/boot
    sudo mount /dev/sdX1 /mnt/boot
    sudo mount /dev/sdX2 /mnt/rootfs
    rm -r /mnt/boot/*
    rm -r /mnt/rootfs/*
    cd /mnt/rootfs
    wget https://github.com/downloads/scottcarr/beagle/wind-beagle-image-rootfs-release.tar.gz
    tar -xzvf wind-beagle-image-rootfs-release.tar.gz 
    cd /mnt/boot
    wget https://github.com/downloads/scottcarr/beagle/wind-beagle-image-boot-release.tar.gz
    tar -xzvf wind-beagle-image-boot-release.tar.gz 
    sudo umount /mnt/rootfs
    sudo umount /mnt/boot

That's it.





