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

CC      =       bcc
CFLAGS  =       -ml -w-pro -O
COCOR   =       ..\cocor.exe

#          *Implicit Rules*
.c.obj:
		$(CC) -c $(CFLAGS) {$< }

all:            Taste.exe Pretty.exe XRef.exe

Taste.exe:      Tastep.obj  TC.obj TL.Obj
		$(CC) $(CFLAGS) -eTaste.exe Taste.obj TL.obj TC.Obj\
					     Tastes.obj Tastep.obj

Tastep.obj:     Taste.Atg
		$(COCOR) Taste.atg
		$(CC) $(CFLAGS) -c Taste.c Tastep.c Tastes.c


Pretty.exe:     Prettyp.obj  Prettypr.obj
		$(CC) $(CFLAGS) -ePretty.exe Pretty.obj PrettyPr.obj \
					     Prettys.obj Prettyp.obj

Prettyp.obj:    Pretty.Atg
		$(COCOR) Pretty.atg
		$(CC) $(CFLAGS) -c Pretty.c Prettyp.c Prettys.c

Xref.exe:       Xrefp.obj  Crossref.obj
		$(CC) $(CFLAGS) -eXref.exe Xref.obj crossref.obj \
					     Xrefs.obj Xrefp.obj

Xrefp.obj:      Xref.Atg
		$(COCOR) Xref.atg
		$(CC) $(CFLAGS) -c Xref.c Xrefp.c Xrefs.c

clean:
		del *.obj
		del Pretty.exe
		del Xref.exe
		del Taste.exe
		del Taste?.c
		del Taste?.h
		del Xref?.c
		del Xref?.h
		del Pretty?.c
		del Pretty?.h
		del *.lst
		del *.bak

