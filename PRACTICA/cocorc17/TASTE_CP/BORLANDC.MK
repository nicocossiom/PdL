# Makefile for Borland C++
# To use this file type "make -f borlandc.mk [entry-point]"
# Entry Points:
# all   (Default) build Taste examples
# new   Clean and build Taste examples
# clean Clean all objects and executable files


# CFLAGS:
# -ml           for large memory model
# -w-pro        suppress the "prototype warning"
# -O            Optimization
# -I            Extra include directory (..\cplus2)
# -L            Extra library directory (..\cplus2) to look for cr_lib.lib

CC      =       bcc
CFLAGS  =       -ml -w-pro -I..\cplus2 -L..\cplus2
COCOR   =       ..\cocor.exe 

#          *Implicit Rules*
.cpp.obj:
		$(CC) -c $(CFLAGS) {$< }


all:            Taste.exe Pretty.exe XRef.exe

Taste.exe:      Tastep.obj  TC.obj TL.Obj
		$(CC) $(CFLAGS) -eTaste.exe Taste.obj TL.obj TC.Obj\
				  Tastes.obj Tastep.obj cr_lib.lib

Tastep.obj:     Taste.Atg
		$(COCOR) Taste.atg
		$(CC) $(CFLAGS) -c Taste.cpp Tastep.cpp Tastes.cpp


Pretty.exe:     Prettyp.obj  Prettypr.obj
		$(CC) $(CFLAGS) -ePretty.exe Pretty.obj PrettyPr.obj \
				  Prettys.obj Prettyp.obj cr_lib.lib

Prettyp.obj:    Pretty.Atg
		$(COCOR) Pretty.atg
		$(CC) $(CFLAGS) -c Pretty.cpp Prettyp.cpp Prettys.cpp

Xref.exe:       Xrefp.obj  Crossref.obj
		$(CC) $(CFLAGS) -eXref.exe Xref.obj crossref.obj \
				  Xrefs.obj Xrefp.obj cr_lib.lib

Xrefp.obj:      Xref.Atg
		$(COCOR) Xref.atg
		$(CC) $(CFLAGS) -c Xref.cpp Xrefp.cpp Xrefs.cpp

clean:
		del *.obj
		del Pretty.exe 
		del Xref.exe 
		del Taste.exe 
		del Taste?.cpp 
		del Taste?.hpp
		del Xref?.cpp
		del Xref?.hpp
		del Pretty?.cpp
		del Pretty?.hpp
		del *.h
		del *.lst
		del *.bak

