# If KERNELREALSE is define, we've been invokes from the
# kernel build system and can use its language.
ifneq ($(KERNELREALSE),)
 	obj-m := hello_mod.o
# Otherwise we were called directly from the command line
# invoke the kernel build system
else
	KERNELDIR ?= /lib/modules/$(shell uname -r)/build
	PWD := $(shell pwd)

default:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules

endif

