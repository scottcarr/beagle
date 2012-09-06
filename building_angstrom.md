Building Angstrom from Scratch
------------------------------

Get the latest angstrom config:

    $ git clone git://github.com/Angstrom-distribution/setup-scripts.git

Get the lastest bitbake:
    $ git clone git://git.openembedded.org/bitbake.git

Build bitbake:
    cd bitbake
    python setup.py build
    sudo python setup.py install

bitbake might need the following packages: make, dockbook-xsl, libxml2-utils,
xsltproc

Install the packages required by OpenEmbedded see:
http://wiki.openembedded.org/index.php/OEandYourDistro#Ubuntu

Build angstrom:
    $ cd ../setup-scripts
    $ ./oebb.sh config beagleboard

You might need to make /bin/sh point to bash:
    $ sudo mv /bin/sh /bin/sh_old
    $ sudo ln -s /bin/bash /bin/sh


 
