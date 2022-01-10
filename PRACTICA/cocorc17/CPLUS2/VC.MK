# Microsoft Developer Studio Generated NMAKE File, Based on cplus2.dsp
!IF "$(CFG)" == ""
CFG=cplus2 - Win32 Debug
!MESSAGE No configuration specified. Defaulting to cplus2 - Win32 Debug.
!ENDIF 

!IF "$(CFG)" != "cplus2 - Win32 Release" && "$(CFG)" != "cplus2 - Win32 Debug"
!MESSAGE Invalid configuration "$(CFG)" specified.
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "cplus2.mak" CFG="cplus2 - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "cplus2 - Win32 Release" (based on "Win32 (x86) Static Library")
!MESSAGE "cplus2 - Win32 Debug" (based on "Win32 (x86) Static Library")
!MESSAGE 
!ERROR An invalid configuration is specified.
!ENDIF 

!IF "$(OS)" == "Windows_NT"
NULL=
!ELSE 
NULL=nul
!ENDIF 

!IF  "$(CFG)" == "cplus2 - Win32 Release"

OUTDIR=.\Release
INTDIR=.\Release
# Begin Custom Macros
OutDir=.\Release
# End Custom Macros

!IF "$(RECURSE)" == "0" 

ALL : "$(OUTDIR)\cplus2.lib"

!ELSE 

ALL : "$(OUTDIR)\cplus2.lib"

!ENDIF 

CLEAN :
	-@erase "$(INTDIR)\Cr_abs.obj"
	-@erase "$(INTDIR)\Cr_error.obj"
	-@erase "$(INTDIR)\Cr_parse.obj"
	-@erase "$(INTDIR)\Cr_scan.obj"
	-@erase "$(INTDIR)\vc50.idb"
	-@erase "$(OUTDIR)\cplus2.lib"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP=cl.exe
CPP_PROJ=/nologo /ML /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_WINDOWS"\
 /Fp"$(INTDIR)\cplus2.pch" /YX /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /c 
CPP_OBJS=.\Release/
CPP_SBRS=.

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

BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\cplus2.bsc" 
BSC32_SBRS= \
	
LIB32=link.exe -lib
LIB32_FLAGS=/nologo /out:"$(OUTDIR)\cplus2.lib" 
LIB32_OBJS= \
	"$(INTDIR)\Cr_abs.obj" \
	"$(INTDIR)\Cr_error.obj" \
	"$(INTDIR)\Cr_parse.obj" \
	"$(INTDIR)\Cr_scan.obj"

"$(OUTDIR)\cplus2.lib" : "$(OUTDIR)" $(DEF_FILE) $(LIB32_OBJS)
    $(LIB32) @<<
  $(LIB32_FLAGS) $(DEF_FLAGS) $(LIB32_OBJS)
<<

!ELSEIF  "$(CFG)" == "cplus2 - Win32 Debug"

OUTDIR=.\Debug
INTDIR=.\Debug
# Begin Custom Macros
OutDir=.\Debug
# End Custom Macros

!IF "$(RECURSE)" == "0" 

ALL : "$(OUTDIR)\cplus2.lib"

!ELSE 

ALL : "$(OUTDIR)\cplus2.lib"

!ENDIF 

CLEAN :
	-@erase "$(INTDIR)\Cr_abs.obj"
	-@erase "$(INTDIR)\Cr_error.obj"
	-@erase "$(INTDIR)\Cr_parse.obj"
	-@erase "$(INTDIR)\Cr_scan.obj"
	-@erase "$(INTDIR)\vc50.idb"
	-@erase "$(OUTDIR)\cplus2.lib"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP=cl.exe
CPP_PROJ=/nologo /MLd /W3 /GX /Z7 /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS"\
 /Fp"$(INTDIR)\cplus2.pch" /YX /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /c 
CPP_OBJS=.\Debug/
CPP_SBRS=.

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

BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\cplus2.bsc" 
BSC32_SBRS= \
	
LIB32=link.exe -lib
LIB32_FLAGS=/nologo /out:"$(OUTDIR)\cplus2.lib" 
LIB32_OBJS= \
	"$(INTDIR)\Cr_abs.obj" \
	"$(INTDIR)\Cr_error.obj" \
	"$(INTDIR)\Cr_parse.obj" \
	"$(INTDIR)\Cr_scan.obj"

"$(OUTDIR)\cplus2.lib" : "$(OUTDIR)" $(DEF_FILE) $(LIB32_OBJS)
    $(LIB32) @<<
  $(LIB32_FLAGS) $(DEF_FLAGS) $(LIB32_OBJS)
<<

!ENDIF 


!IF "$(CFG)" == "cplus2 - Win32 Release" || "$(CFG)" == "cplus2 - Win32 Debug"
SOURCE=.\Cr_abs.cpp

"$(INTDIR)\Cr_abs.obj" : $(SOURCE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


SOURCE=.\Cr_error.cpp

!IF  "$(CFG)" == "cplus2 - Win32 Release"

DEP_CPP_CR_ER=\
	".\cr_abs.hpp"\
	".\cr_error.hpp"\
	

"$(INTDIR)\Cr_error.obj" : $(SOURCE) $(DEP_CPP_CR_ER) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "cplus2 - Win32 Debug"

DEP_CPP_CR_ER=\
	".\cr_abs.hpp"\
	".\cr_error.hpp"\
	

"$(INTDIR)\Cr_error.obj" : $(SOURCE) $(DEP_CPP_CR_ER) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=.\Cr_parse.cpp

!IF  "$(CFG)" == "cplus2 - Win32 Release"

DEP_CPP_CR_PA=\
	".\cr_abs.hpp"\
	".\cr_error.hpp"\
	".\cr_parse.hpp"\
	

"$(INTDIR)\Cr_parse.obj" : $(SOURCE) $(DEP_CPP_CR_PA) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "cplus2 - Win32 Debug"

DEP_CPP_CR_PA=\
	".\cr_abs.hpp"\
	".\cr_error.hpp"\
	".\cr_parse.hpp"\
	

"$(INTDIR)\Cr_parse.obj" : $(SOURCE) $(DEP_CPP_CR_PA) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=.\Cr_scan.cpp

!IF  "$(CFG)" == "cplus2 - Win32 Release"

DEP_CPP_CR_SC=\
	".\cr_abs.hpp"\
	".\cr_scan.hpp"\
	

"$(INTDIR)\Cr_scan.obj" : $(SOURCE) $(DEP_CPP_CR_SC) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "cplus2 - Win32 Debug"

DEP_CPP_CR_SC=\
	".\cr_abs.hpp"\
	".\cr_scan.hpp"\
	

"$(INTDIR)\Cr_scan.obj" : $(SOURCE) $(DEP_CPP_CR_SC) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 


!ENDIF 

