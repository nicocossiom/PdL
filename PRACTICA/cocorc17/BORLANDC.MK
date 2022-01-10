# Makefile for using with Borland C++ 3.1
# To use this file type "make -f borlandc.mk [entry-point]"
# Entry Points:
# all   (Default) build cocor
# new   Clean and build cocor
# clean Clean all objects and executable files

MAKE   = make

all:
		cd coco2msg
		$(MAKE) -f borlandc.mk
		cd ..
		cd sources
		$(MAKE) -f borlandc.mk
		cd ..
		cd taste
		$(MAKE) -f borlandc.mk
		cd ..
		cd cplus2
		$(MAKE) -f borlandc.mk
		cd ..
		cd taste_cp
		$(MAKE) -f borlandc.mk
		cd ..

clean:
		cd coco2msg
		$(MAKE) -f borlandc.mk clean
		cd ..
		cd sources
		$(MAKE) -f borlandc.mk clean
		cd ..
		cd taste
		$(MAKE) -f borlandc.mk clean
		cd ..
		cd cplus2
		$(MAKE) -f borlandc.mk clean
		cd ..
		cd taste_cp
		$(MAKE) -f borlandc.mk clean
		cd ..
