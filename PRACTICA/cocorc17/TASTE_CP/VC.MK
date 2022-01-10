# Microsoft Developer Studio Generated NMAKE File, Based on taste_cp.dsp
!IF "$(CFG)" == ""
CFG=taste_cp - Win32 Debug
!MESSAGE No configuration specified. Defaulting to taste_cp - Win32 Debug.
!ENDIF 

!IF "$(CFG)" != "taste_cp - Win32 Release" && "$(CFG)" !=\
 "taste_cp - Win32 Debug"
!MESSAGE Invalid configuration "$(CFG)" specified.
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "taste_cp.mak" CFG="taste_cp - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "taste_cp - Win32 Release" (based on\
 "Win32 (x86) Console Application")
!MESSAGE "taste_cp - Win32 Debug" (based on "Win32 (x86) Console Application")
!MESSAGE 
!ERROR An invalid configuration is specified.
!ENDIF 

!IF "$(OS)" == "Windows_NT"
NULL=
!ELSE 
NULL=nul
!ENDIF 

!IF  "$(CFG)" == "taste_cp - Win32 Release"

OUTDIR=.\Release
INTDIR=.\Release
# Begin Custom Macros
OutDir=.\Release
# End Custom Macros

!IF "$(RECURSE)" == "0" 

ALL : "$(OUTDIR)\taste_cp.exe"

!ELSE 

ALL : "$(OUTDIR)\taste_cp.exe"

!ENDIF 

CLEAN :
	-@erase "$(INTDIR)\taste.obj"
	-@erase "$(INTDIR)\tastep.obj"
	-@erase "$(INTDIR)\tastes.obj"
	-@erase "$(INTDIR)\Tc.obj"
	-@erase "$(INTDIR)\Tl.obj"
	-@erase "$(INTDIR)\vc50.idb"
	-@erase "$(OUTDIR)\taste_cp.exe"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP=cl.exe
CPP_PROJ=/nologo /ML /W3 /GX /O2 /I "C:\MyPrograms\CocorC1.07\cplus2" /D\
 "WIN32" /D "NDEBUG" /D "_CONSOLE" /D "_MBCS" /Fp"$(INTDIR)\taste_cp.pch" /YX\
 /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /c 
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

RSC=rc.exe
BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\taste_cp.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
LINK32_FLAGS=C:\MyPrograms\CocorC1.07\cplus2\cplus2.lib kernel32.lib user32.lib\
 gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib\
 oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:console\
 /incremental:no /pdb:"$(OUTDIR)\taste_cp.pdb" /machine:I386\
 /out:"$(OUTDIR)\taste_cp.exe" 
LINK32_OBJS= \
	"$(INTDIR)\taste.obj" \
	"$(INTDIR)\tastep.obj" \
	"$(INTDIR)\tastes.obj" \
	"$(INTDIR)\Tc.obj" \
	"$(INTDIR)\Tl.obj"

"$(OUTDIR)\taste_cp.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ELSEIF  "$(CFG)" == "taste_cp - Win32 Debug"

OUTDIR=.\Debug
INTDIR=.\Debug
# Begin Custom Macros
OutDir=.\Debug
# End Custom Macros

!IF "$(RECURSE)" == "0" 

ALL : "$(OUTDIR)\taste_cp.exe"

!ELSE 

ALL : "$(OUTDIR)\taste_cp.exe"

!ENDIF 

CLEAN :
	-@erase "$(INTDIR)\taste.obj"
	-@erase "$(INTDIR)\tastep.obj"
	-@erase "$(INTDIR)\tastes.obj"
	-@erase "$(INTDIR)\Tc.obj"
	-@erase "$(INTDIR)\Tl.obj"
	-@erase "$(INTDIR)\vc50.idb"
	-@erase "$(INTDIR)\vc50.pdb"
	-@erase "$(OUTDIR)\taste_cp.exe"
	-@erase "$(OUTDIR)\taste_cp.ilk"
	-@erase "$(OUTDIR)\taste_cp.pdb"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP=cl.exe
CPP_PROJ=/nologo /MLd /W3 /Gm /GX /Zi /Od /I "C:\MyPrograms\CocorC1.07\cplus2"\
 /D "WIN32" /D "_DEBUG" /D "_CONSOLE" /D "_MBCS" /Fp"$(INTDIR)\taste_cp.pch" /YX\
 /Fo"$(INTDIR)\\" /Fd"$(INTDIR)\\" /FD /c 
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

RSC=rc.exe
BSC32=bscmake.exe
BSC32_FLAGS=/nologo /o"$(OUTDIR)\taste_cp.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
LINK32_FLAGS=C:\MyPrograms\CocorC1.07\cplus2\cplus2.lib kernel32.lib user32.lib\
 gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib\
 oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:console\
 /profile /debug /machine:I386 /out:"$(OUTDIR)\taste_cp.exe" 
LINK32_OBJS= \
	"$(INTDIR)\taste.obj" \
	"$(INTDIR)\tastep.obj" \
	"$(INTDIR)\tastes.obj" \
	"$(INTDIR)\Tc.obj" \
	"$(INTDIR)\Tl.obj"

"$(OUTDIR)\taste_cp.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ENDIF 


!IF "$(CFG)" == "taste_cp - Win32 Release" || "$(CFG)" ==\
 "taste_cp - Win32 Debug"
SOURCE=..\taste.cpp

!IF  "$(CFG)" == "taste_cp - Win32 Release"

DEP_CPP_TASTE=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\..\cplus2\cr_parse.hpp"\
	"..\..\cplus2\cr_scan.hpp"\
	"..\tastee.hpp"\
	"..\tastep.hpp"\
	"..\tastes.hpp"\
	"..\tc.hpp"\
	"..\tl.hpp"\
	

"$(INTDIR)\taste.obj" : $(SOURCE) $(DEP_CPP_TASTE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "taste_cp - Win32 Debug"

DEP_CPP_TASTE=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\..\cplus2\cr_parse.hpp"\
	"..\..\cplus2\cr_scan.hpp"\
	"..\tastee.hpp"\
	"..\tastep.hpp"\
	"..\tastes.hpp"\
	"..\tc.hpp"\
	"..\tl.hpp"\
	

"$(INTDIR)\taste.obj" : $(SOURCE) $(DEP_CPP_TASTE) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=..\tastep.cpp

!IF  "$(CFG)" == "taste_cp - Win32 Release"

DEP_CPP_TASTEP=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\..\cplus2\cr_parse.hpp"\
	"..\..\cplus2\cr_scan.hpp"\
	"..\tastec.hpp"\
	"..\tastep.hpp"\
	"..\tastes.hpp"\
	"..\tc.hpp"\
	"..\tl.hpp"\
	

"$(INTDIR)\tastep.obj" : $(SOURCE) $(DEP_CPP_TASTEP) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "taste_cp - Win32 Debug"

DEP_CPP_TASTEP=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\..\cplus2\cr_parse.hpp"\
	"..\..\cplus2\cr_scan.hpp"\
	"..\tastec.hpp"\
	"..\tastep.hpp"\
	"..\tastes.hpp"\
	"..\tc.hpp"\
	"..\tl.hpp"\
	

"$(INTDIR)\tastep.obj" : $(SOURCE) $(DEP_CPP_TASTEP) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=..\tastes.cpp

!IF  "$(CFG)" == "taste_cp - Win32 Release"

DEP_CPP_TASTES=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_scan.hpp"\
	"..\tastec.hpp"\
	"..\tastes.hpp"\
	

"$(INTDIR)\tastes.obj" : $(SOURCE) $(DEP_CPP_TASTES) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "taste_cp - Win32 Debug"

DEP_CPP_TASTES=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_scan.hpp"\
	"..\tastec.hpp"\
	"..\tastes.hpp"\
	

"$(INTDIR)\tastes.obj" : $(SOURCE) $(DEP_CPP_TASTES) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 

SOURCE=..\Tc.cpp
DEP_CPP_TC_CP=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\tc.hpp"\
	

"$(INTDIR)\Tc.obj" : $(SOURCE) $(DEP_CPP_TC_CP) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


SOURCE=..\Tl.cpp

!IF  "$(CFG)" == "taste_cp - Win32 Release"

DEP_CPP_TL_CP=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\tl.hpp"\
	

"$(INTDIR)\Tl.obj" : $(SOURCE) $(DEP_CPP_TL_CP) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ELSEIF  "$(CFG)" == "taste_cp - Win32 Debug"

DEP_CPP_TL_CP=\
	"..\..\cplus2\cr_abs.hpp"\
	"..\..\cplus2\cr_error.hpp"\
	"..\tl.hpp"\
	

"$(INTDIR)\Tl.obj" : $(SOURCE) $(DEP_CPP_TL_CP) "$(INTDIR)"
	$(CPP) $(CPP_PROJ) $(SOURCE)


!ENDIF 


!ENDIF 

