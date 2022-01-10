# Makefile for using with Borland C++ 5.5
# To use this file type "make -f borlandc.mk [entry-point]"
# Entry Points:
# all   (Default) build cocor c++ library
# clean Clean all objects and executable files

# CFLAGS:
# -ml           for large memory model
# -w-pro        suppress the "prototype warning"
# -O            Optimization

CC      =       bcc32
LIB     =       tlib
CFLAGS  =       -w-pro -O

all:            cr_lib.lib

cr_lib.lib:
		$(CC) $(CFLAGS) -c cr_abs.cpp cr_error.cpp \
			cr_scan.cpp cr_parse.cpp
		$(LIB) cr_lib.lib +cr_abs.obj + cr_error.obj \
		       +cr_scan.obj +cr_parse.obj

clean:
		del *.obj
		del *.lib
		del *.bak

