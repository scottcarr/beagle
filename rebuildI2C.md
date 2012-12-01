#Re-building Angstrom for 400kHz I2C

##DISCLAIMER 1

I've decided to use Yocto/Poky because I always end up running into errors
with Angstrom.  Angstrom does have a better default package set though.

##DISCLAIMER 2 

This is a sort of hackish way to accomplish what we need.  Making
our own layer would be better/more sustainable, but it'd also be a lot more work.
I'll try to work on that over break.

Execute these commands:

    git clone git://git.yoctoproject.org/poky 
    cd poky
    git clone git://git.yoctoproject.org/meta-ti
    source oe-init-build-env beaglebone

You should now be in a directory called beaglebone

Uncomment the following lines in conf/local.conf:

    BB_NUMBER_THREADS = "4"

    PARALLEL_MAKE = "-j 4"

You can change the number of threads if you want.

Add this line in conf/local.conf:
    MACHINE ?= "beaglebone"

Add the meta-ti layer to conf/bblayers.conf and mask meta-ti/recipes-misc.  It 
should look like:

    # LAYER_CONF_VERSION is increased each time build/conf/bblayers.conf
    # changes incompatibly
    LCONF_VERSION = "6"

    BBPATH = "${TOPDIR}"
    BBFILES ?= ""

    BBLAYERS ?= " \
      /home/scott/poky/meta \
      /home/scott/poky/meta-yocto \
      /home/scott/poky/meta-yocto-bsp \
      /home/scott/poky/meta-ti \    
      "
    BBLAYERS_NON_REMOVABLE ?= " \
      /home/scott/poky/meta \
      /home/scott/poky/meta-yocto \
      "

    BBMASK = "meta-ti/recipes-misc"

Note: it says you need to do that BBMASK in meta-ti/README, so that's why
we do it.

Add the folliwing line to poky/meta/recipes-exteneded/images/core-image-lsb-sdk

    IMAGE_INSTALL += "git"
    # you can add more packages to IMAGE_INSTALL if you want
    # it'll work if poky knows that package, otherwise you'll
    # get an error when you try to build

It should look like:
    DESCRIPTION = "Basic image without X support suitable for Linux Standard Base \
    (LSB) implementations. It includes the full meta-toolchain, plus development \
    headers and libraries to form a standalone SDK."

    IMAGE_FEATURES += "splash tools-sdk dev-pkgs ssh-server-openssh \
        tools-debug tools-profile tools-testapps debug-tweaks"


    IMAGE_INSTALL = "\
        ${CORE_IMAGE_BASE_INSTALL} \
        packagegroup-core-basic \
        packagegroup-core-lsb \
        kernel-dev \
        "

    IMAGE_INSTALL += "git"

    inherit core-image

You need to change something to get the correct I2C speed.  You need
to edit:

    poky/meta-ti/recipes-kernel/linux/linux-ti33x-psp-3.2/beaglebone/0003-beaglebone-rebase-everything-onto-3.2-WARNING-MEGAPA.patch

Change:

    521 +        setup_pin_mux(i2c2_pin_mux);
    522 +        omap_register_i2c_bus(3, 100, cape_i2c_boardinfo,
    523 +                        ARRAY_SIZE(cape_i2c_boardinfo));
    524 +        return;

To:

    521 +        setup_pin_mux(i2c2_pin_mux);
    522 +        omap_register_i2c_bus(3, 400, cape_i2c_boardinfo,
    523 +                        ARRAY_SIZE(cape_i2c_boardinfo));
    524 +        return;

Go back to the poky/beaglebone directory and run:

    bitbake core-image-lsb-sdk

##Optional: Try the demo image to make sure your hardware works

You can skip this step if you've already got a correctly partitioned SD
card and your know your hardware setup works.

Get the Angstrom BeagleBone demo image from [here.](http://downloads.angstrom-distribution.org/demo/beaglebone/)

Download Angstrom-Cloud9-IDE-GNOME-eglibc-ipk-v2012.05-beaglebone-2012.09.12.img.xz  
and follow the instructions under "How to Unpack and Boot the Demo Image - easy way."

Your SD card is now setup correctly to run the demo image.  You can
go ahead and try it out as a sanity check.  Eject the SD card and put it
in the beaglebone.

Log into the beaglebone. On Linux you do:

    sudo screen /dev/ttyUSB1 115200

Remember Control-A k kills screen.

If you can log into the beaglebone the sanity check passed.  

Assuming all goes well, when your build finishes, you can just overwrite with
your own files and be good-to-go.

## When bitbake core-image-lsb-sdk finishes

Remove the SD card from the beaglebone and put it back in your computer. 

Mount the root file system partition of your SD card (maybe /dev/sdb2) as /mnt/rootfs.
Loading the Angstrom demo image partitions the SD card for you.  The first
partition is boot and the second is the root file system.
<!--- Mount the second partition (maybe /dev/sdb2) as /mnt/rootfs
-->

Deploy the rootfs to that partition:

    cd poky/beaglebone/tmp/deploy/images
    sudo rm -r /mnt/rootfs/* # clear our the old rootfs
    sudo tar -xjv -C /mnt/rootfs -f core-image-lsb-sdk-beaglebone.tar.bz2
    sudo tar -xzv -C /mnt/rootfs -f modules-beaglebone.tgz

<---
Deploy the boot partition:

    cd poky/beaglebone/tmp/deploy/images
    sudo cp MLO /mnt/boot/
    sudo cp MLO /mnt/rootfs/boot
    sudo cp u-boot.img /mnt/boot/
    sudo cp u-boot.img /mnt/rootfs/boot/
    sudo cp uImage /mnt/boot/
    sudo cp u-boot.img /mnt/rootfs/boot/
-->

Unmount the SD card and eject it. Put the SD card back in the beaglebone and boot it.

It will take a while to boot the first time.

Log into the beaglebone and type:

    dmesg | grep i2c

If you get back:
    [    0.102813]  omap_i2c.1: alias fck already exists
    [    0.118530] omap_i2c omap_i2c.1: bus 1 rev2.4.0 at 100 kHz
    [    0.253784]  omap_i2c.3: alias fck already exists
    [    0.254089] omap_i2c omap_i2c.3: bus 3 rev2.4.0 at 400 kHz
    [    0.544921] i2c /dev entries driver

You're now running I2C 3 at 400kHz (max speed for the MPU6050).

For instructions on how to run the MPU6050 app go [here](MPU6050_app.md)







