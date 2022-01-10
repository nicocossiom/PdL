# Makefile for using with Borland C++ 3.1
# To use this file type "make -f borlandc.mk [entry-point]"
# Entry Points:
# all   (Default) build cocor
# new   Clean and build cocor
# clean Clean all objects and executable files


# CFLAGS:
# -ml           for large memory model
# -w-pro        suppress the "prototype warning"
# -O            Optimization
#
# add the following if necessary
# -DDebug=1     Enable ASSERT macro for help in tracking memory leaks

CFLAGS  = -ml -w-pro -O
CC      = bcc

SRCS = \
	cr.c \
	cra.c \
	crp.c \
	crs.c \
	crt.c \
	crx.c \
	crf.c \
	collect.c \
	set.c

OBJS = \
	cr.obj \
	cra.obj \
	crp.obj \
	crs.obj \
	crt.obj \
	crx.obj \
	crf.obj \
	collect.obj\
	set.obj

#          *Implicit Rules*
.c.obj:
		$(CC) -c $(CFLAGS) {$< }


all:            cocor.exe

new:            clean cocor.exe

cocor.exe:      $(OBJS)
		$(CC) -ecocor.exe $(CFLAGS) $(OBJS)
		copy cocor.exe ..

clean:
		del *.obj
		del cocor.exe 
		del *.bak

