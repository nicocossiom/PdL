# Microsoft Developer Studio Generated NMAKE File, Based on sources.dsp
!IF "$(CFG)" == ""
CFG=cocor - Win32 Debug
!MESSAGE No configuration specified. Defaulting to sources - Win32 Debug.
!ENDIF 

!IF "$(CFG)" != "cocor - Win32 Release" && "$(CFG)" !=\
 "cocor - Win32 Debug"
!MESSAGE Invalid configuration "$(CFG)" specified.
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "vc.mak" CFG="cocor - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "cocor - Win32 Release" (based on "Win32 (x86) Console Application")
!MESSAGE "cocor - Win32 Debug" (based on "Win32 (x86) Console Application")
!MESSAGE 
!ERROR An invalid configuration is specified.
!ENDIF 

!IF "$(OS)" == "Windows_NT"
NULL=
!ELSE 
NULL=nul
!ENDIF 

CPP=cl.exe
RSC=rc.exe

!IF  "$(CFG)" == "cocor - Win32 Release"

OUTDIR=.\Release
INTDIR=.\Release
# Begin Custom Macros
OutDir=.\Release
# End Custom Macros

!IF "$(RECURSE)" == "0" 

ALL : "$(OUTDIR)\cocor.exe"

!ELSE 

ALL : "$(OUTDIR)\cocor.exe"

!ENDIF 

CLEAN :
	-@erase "$(INTDIR)\Collect.obj"
	-@erase "$(INTDIR)\Cr.obj"
	-@erase "$(INTDIR)\Cra.obj"
	-@erase "$(INTDIR)\Crf.obj"
	-@erase "$(INTDIR)\Crp.obj"
	-@erase "$(INTDIR)\Crs.obj"
	-@erase "$(INTDIR)\Crt.obj"
	-@erase "$(INTDIR)\Crx.obj"
	-@erase "$(INTDIR)\Set.obj"
	-@erase "$(INTDIR)\vc50.idb"
	-@erase "$(OUTDIR)\cocor.exe"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP_PROJ=/nologo /ML /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /D\
 "_MBCS" /Fp"$(INTDIR)\cocor.pch" /YX /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /c\
 
CPP_OBJS=.\Release/
CPP_SBRS=.
BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\cocor.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
LINK32_FLAGS=kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib\
 advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib\
 odbccp32.lib /nologo /subsystem:console /incremental:no\
 /pdb:"$(OUTDIR)\cocor.pdb" /machine:I386 /out:"$(OUTDIR)\cocor.exe" 
LINK32_OBJS= \
	"$(INTDIR)\Collect.obj" \
	"$(INTDIR)\Cr.obj" \
	"$(INTDIR)\Cra.obj" \
	"$(INTDIR)\Crf.obj" \
	"$(INTDIR)\Crp.obj" \
	"$(INTDIR)\Crs.obj" \
	"$(INTDIR)\Crt.obj" \
	"$(INTDIR)\Crx.obj" \
	"$(INTDIR)\Set.obj"

"$(OUTDIR)\cocor.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

OUTDIR=.\Debug
INTDIR=.\Debug
# Begin Custom Macros
OutDir=.\Debug
# End Custom Macros

!IF "$(RECURSE)" == "0" 

ALL : "$(OUTDIR)\cocor.exe"

!ELSE 

ALL : "$(OUTDIR)\cocor.exe"

!ENDIF 

CLEAN :
	-@erase "$(INTDIR)\Collect.obj"
	-@erase "$(INTDIR)\Cr.obj"
	-@erase "$(INTDIR)\Cra.obj"
	-@erase "$(INTDIR)\Crf.obj"
	-@erase "$(INTDIR)\Crp.obj"
	-@erase "$(INTDIR)\Crs.obj"
	-@erase "$(INTDIR)\Crt.obj"
	-@erase "$(INTDIR)\Crx.obj"
	-@erase "$(INTDIR)\Set.obj"
	-@erase "$(INTDIR)\vc50.idb"
	-@erase "$(INTDIR)\vc50.pdb"
	-@erase "$(OUTDIR)\cocor.exe"
	-@erase "$(OUTDIR)\cocor.ilk"
	-@erase "$(OUTDIR)\cocor.pdb"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP_PROJ=/nologo /MLd /W3 /Gm /GX /Zi /Od /D "WIN32" /D "_DEBUG" /D "_CONSOLE"\
 /D "_MBCS" /Fp"$(INTDIR)\cocor.pch" /YX /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD\
 /c 
CPP_OBJS=.\Debug/
CPP_SBRS=.
BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\cocor.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
LINK32_FLAGS=kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib\
 advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib\
 odbccp32.lib /nologo /subsystem:console /incremental:yes\
 /pdb:"$(OUTDIR)\cocor.pdb" /debug /machine:I386 /out:"$(OUTDIR)\sources.exe"\
 /pdbtype:sept 
LINK32_OBJS= \
	"$(INTDIR)\Collect.obj" \
	"$(INTDIR)\Cr.obj" \
	"$(INTDIR)\Cra.obj" \
	"$(INTDIR)\Crf.obj" \
	"$(INTDIR)\Crp.obj" \
	"$(INTDIR)\Crs.obj" \
	"$(INTDIR)\Crt.obj" \
	"$(INTDIR)\Crx.obj" \
	"$(INTDIR)\Set.obj"

"$(OUTDIR)\cocor.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ENDIF 

.c{$(CPP_OBJS)}.obj::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cpp{$(CPP_OBJS)}.obj::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cxx{$(CPP_OBJS)}.obj::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.c{$(CPP_SBRS)}.sbr::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cpp{$(CPP_SBRS)}.sbr::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<

.cxx{$(CPP_SBRS)}.sbr::
   $(CPP) @<<
   $(CPP_PROJ) $< 
<<


!IF "$(CFG)" == "cocor - Win32 Release" || "$(CFG)" ==\
 "cocor - Win32 Debug"
SOURCE=.\Collect.c
DEP_CPP_COLLE=\
	".\collect.h"\
	

"$(INTDIR)\Collect.obj" : $(SOURCE) $(DEP_CPP_COLLE) "$(INTDIR)"


SOURCE=.\Cr.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CR_C2=\
	".\collect.h"\
	".\cra.h"\
	".\crc.h"\
	".\cre.h"\
	".\crf.h"\
	".\crp.h"\
	".\crs.h"\
	".\crt.h"\
	".\crx.h"\
	".\set.h"\
	

"$(INTDIR)\Cr.obj" : $(SOURCE) $(DEP_CPP_CR_C2) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CR_C2=\
	".\collect.h"\
	".\cra.h"\
	".\crc.h"\
	".\cre.h"\
	".\crf.h"\
	".\crp.h"\
	".\crs.h"\
	".\crt.h"\
	".\crx.h"\
	".\set.h"\
	

"$(INTDIR)\Cr.obj" : $(SOURCE) $(DEP_CPP_CR_C2) "$(INTDIR)"


!ENDIF 

SOURCE=.\Cra.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CRA_C=\
	".\collect.h"\
	".\cra.h"\
	".\crf.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Cra.obj" : $(SOURCE) $(DEP_CPP_CRA_C) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CRA_C=\
	".\collect.h"\
	".\cra.h"\
	".\crf.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Cra.obj" : $(SOURCE) $(DEP_CPP_CRA_C) "$(INTDIR)"


!ENDIF 

SOURCE=.\Crf.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CRF_C=\
	".\collect.h"\
	".\crf.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Crf.obj" : $(SOURCE) $(DEP_CPP_CRF_C) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CRF_C=\
	".\collect.h"\
	".\crf.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Crf.obj" : $(SOURCE) $(DEP_CPP_CRF_C) "$(INTDIR)"


!ENDIF 

SOURCE=.\Crp.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CRP_C=\
	".\collect.h"\
	".\cra.h"\
	".\crc.h"\
	".\crf.h"\
	".\crp.h"\
	".\crs.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Crp.obj" : $(SOURCE) $(DEP_CPP_CRP_C) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CRP_C=\
	".\collect.h"\
	".\cra.h"\
	".\crc.h"\
	".\crf.h"\
	".\crp.h"\
	".\crs.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Crp.obj" : $(SOURCE) $(DEP_CPP_CRP_C) "$(INTDIR)"


!ENDIF 

SOURCE=.\Crs.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CRS_C=\
	".\crc.h"\
	".\crs.h"\
	{$(INCLUDE)}"sys\types.h"\
	

"$(INTDIR)\Crs.obj" : $(SOURCE) $(DEP_CPP_CRS_C) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CRS_C=\
	".\crc.h"\
	".\crs.h"\
	

"$(INTDIR)\Crs.obj" : $(SOURCE) $(DEP_CPP_CRS_C) "$(INTDIR)"


!ENDIF 

SOURCE=.\Crt.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CRT_C=\
	".\collect.h"\
	".\cra.h"\
	".\crc.h"\
	".\crf.h"\
	".\crs.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Crt.obj" : $(SOURCE) $(DEP_CPP_CRT_C) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CRT_C=\
	".\collect.h"\
	".\cra.h"\
	".\crc.h"\
	".\crf.h"\
	".\crs.h"\
	".\crt.h"\
	".\set.h"\
	

"$(INTDIR)\Crt.obj" : $(SOURCE) $(DEP_CPP_CRT_C) "$(INTDIR)"


!ENDIF 

SOURCE=.\Crx.c

!IF  "$(CFG)" == "cocor - Win32 Release"

DEP_CPP_CRX_C=\
	".\collect.h"\
	".\crc.h"\
	".\crf.h"\
	".\crs.h"\
	".\crt.h"\
	".\crx.h"\
	".\set.h"\
	

"$(INTDIR)\Crx.obj" : $(SOURCE) $(DEP_CPP_CRX_C) "$(INTDIR)"


!ELSEIF  "$(CFG)" == "cocor - Win32 Debug"

DEP_CPP_CRX_C=\
	".\collect.h"\
	".\crc.h"\
	".\crf.h"\
	".\crs.h"\
	".\crt.h"\
	".\crx.h"\
	".\set.h"\
	

"$(INTDIR)\Crx.obj" : $(SOURCE) $(DEP_CPP_CRX_C) "$(INTDIR)"


!ENDIF 

SOURCE=.\Set.c
DEP_CPP_SET_C=\
	".\set.h"\
	

"$(INTDIR)\Set.obj" : $(SOURCE) $(DEP_CPP_SET_C) "$(INTDIR)"



!ENDIF 

