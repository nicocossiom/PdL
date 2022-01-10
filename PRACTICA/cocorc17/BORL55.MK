# Makefile for using with Borland C++ 5.5
# To use this file type "make -f borl55.mk [entry-point]"
# Entry Points:
# all   (Default) build cocor
# new   Clean and build cocor
# clean Clean all objects and executable files

MAKE   = make

all:
		cd coco2msg
                $(MAKE) -f borl55.mk
		cd ..
		cd sources
                $(MAKE) -f borl55.mk
		cd ..
		cd taste
                $(MAKE) -f borl55.mk
		cd ..
		cd cplus2
                $(MAKE) -f borl55.mk
		cd ..
		cd taste_cp
                $(MAKE) -f borl55.mk
		cd ..

clean:
		cd coco2msg
                $(MAKE) -f borl55.mk clean
		cd ..
		cd sources
                $(MAKE) -f borl55.mk clean
		cd ..
		cd taste
                $(MAKE) -f borl55.mk clean
		cd ..
		cd cplus2
                $(MAKE) -f borl55.mk clean
		cd ..
		cd taste_cp
                $(MAKE) -f borl55.mk clean
		cd ..
