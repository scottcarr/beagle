#Building your own image with Yocto

First, all the available embedded Linux tools are a weird interdependent mismash of each other.
Each incoporates BitBake and OpenEmbedded at some level. Angstrom and 
Poky wrap those tools in their own way.  Yocto is the top most layer of all.
The good news is Yocto is sponsored by the Linux Foundation, so it has a reasonably
coherent website and documentation.  Confusingly, there is no code called
Yocto.  It's just an umbrella documentation site.

If you want to read documentation, start with the
 [Yocto Quick Start](https://www.yoctoproject.org/docs/current/yocto-project-qs/yocto-project-qs.html) 

To make an image for the BeagleBone:

    ~$ git clone git://git.yoctoproject.org/poky 
    ~$ cd poky
    ~/poky$ git clone git://git.yoctoproject.org/meta-ti
    ~/poky$ source oe-init-build-env beaglebone

The last command should move you the poky/beaglebone directory.  Here,
there is a directory called conf with two important files, bblayers.conf
and local.conf

In local.conf, you want to add a line MACHINE ?= "beaglebone" and set
BB_NUMBER_THREADS = "4" and PARALLEL_MAKE = "-j 4".  Change 4 to 8 if you
have a quadcore, or 4 to 2 if you have a single core processor.

If you're wondering about the weird ?= operator, in bitbake that sets
the default value of an variable.  If you want to dig into the BitBake
documentation,  for more information see the bitbake documentation
under poky/bitbake/doc/manual.

Now add the meta-ti layer to your bblayers.conf.  It should look similar to:

        # LAYER_CONF_VERSION is increased each time build/conf/bblayers.conf
        # changes incompatibly
        LCONF_VERSION = "4"

        BBFILES ?= ""
        BBLAYERS ?= " \
          /media/scratch/poky-git/meta \
          /media/scratch/poky-git/meta-yocto \
          /media/scratch/poky-git/meta-ti \
          "

A layer is a collection of scripts that add some functionality to the built
image.  In the case of meta-ti, this layer adds the hardware specific parts
we need for the BeagleBone.  FYI, Texas Instruments or ti is the manufacturer
of the BeagleBone.

To build that smallest bootable image possible run:
    
    ~/poky/beagelbone$ bitbake core-image-minimal

The output will be under ~/poky/beaglebone/tmp/deploy/images.  The important
files are core-image-minimal-beaglebone-20121117162657.rootfs.tar.bz2 and
uImage.

core-image-minimal is the root file system.  It goes in the second partition
of the SD card.

uImage is some sort of boot image and goes in the first partition of the SD
card.  !!! ADD BETTER EXPLANATION !!!

To deploy the rootfs image to your SD card, mount the second partion to /media/rootfs and use the command:

    ~/poky/beaglebone/tmp/deploy/images$ sudo tar -xjv -C /media/rootfs -f core-image-minimal*rootfs.tar.bz2

The above command will take several minutes.

To deploy uImage simply copy it to the first partition by any means.

Now, put the SD card in the BeagleBone and plug it in.  Connect to the console with:
    
    $ sudo screen /dev/ttyUSB1 115200

You can kill screen with Control-A + k.  For more information on screen,
see [this tutorial.](http://www.rackaid.com/resources/linux-screen-tutorial-and-how-to/)

Once you're logged into the BeagleBone, you can use uname -a to verify
it is running your recently built kernel.

##Fixing the I2C speed

I modified:

    ~/poky/meta-ti/recipes-kernel/linux/linux-ti33x-psp-3.2/beaglebone/0003-beaglebone-rebase-everything-onto-3.2-WARNING-MEGAPA.patch

the temp src file is:
    ~/poky/beaglebone/tmp/work/beaglebone-poky-linux-gnueabi/linux-ti33x-psp-3.2.28-r0/git/arch/arm/mach-omap2/board-am335xevm.c

I verified that the 400 kHz setting:

    root@beaglebone:~# dmesg | grep i2c
    [    0.102844]  omap_i2c.1: alias fck already exists
    [    0.118499] omap_i2c omap_i2c.1: bus 1 rev2.4.0 at 100 kHz
    [    0.253753]  omap_i2c.3: alias fck already exists
    [    0.254058] omap_i2c omap_i2c.3: bus 3 rev2.4.0 at 400 kHz
    [    0.544891] i2c /dev entries driver

##Adding useful tools

I added:
    IMAGE_FEATURES += "dev-pkgs tools-sdk \
            tools-debug tools-profile tools-testapps debug-tweaks ssh-server-openssh"

to poky/meta/recipes-core/images/core-image-base.bb

To make an sdk:

    ~/poky/beaglebone$ bitbake meta-toolchain-sdk

It will but an executable in ~/poky/beaglebone/tmp/deploy/sdk.  Just run it
and it will unpack in /opt.  Now, source the script there to do
cross compiling.
