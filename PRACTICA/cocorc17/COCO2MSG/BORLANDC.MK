# Makefile for using with Borland C++ 3.1
# To use this file type "make -f borlandc.mk [entry-point]"
# Entry Points:
# all   (Default) build coco2msg
# clean Clean all objects and executable files

# CFLAGS:
# -ml           for large memory model
# -w-pro        suppress the "prototype warning"
# -O            Optimization

CFLAGS  = -ml -w-pro -O
CC      = bcc

#          *Implicit Rules*
.c.obj:
		$(CC) -c $(CFLAGS) {$< }

all:            coco2msg.exe

coco2msg.exe:   coco2msg.obj
		$(CC)  $(CFLAGS) -ecoco2msg.exe coco2msg.obj

clean:
		del *.obj
		del *.exe 





















