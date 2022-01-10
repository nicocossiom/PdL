/*
  SOURCE CODE FOR COCO2MSG FILTER

  Coco2Msg.C
  Adapted from Borland Sample by Frankie Arzu.
  Compiler:  Borland C++ 3.1

  Coco2Msg - Message filter from Coco to the IDE message window.

  This filter accepts input through the standard input stream, converts
  it and outputs it to the standard output stream.  The streams are linked
  through pipes, such that the input stream is the output from COCO, and
  the output stream is connected to the message window of the IDE.
  This filter is invoked through the IDE transfer mechanism as

        cocor <commands> | coco2msg | IDE message window

  Since cocor does not write its output to stdout but to stderr,
  I had to do a little trick to fool the IDE.
  First compile coco2msg.c to generate coco2msg.exe, then copy coco2msg.exe to
  &coco2msg.exe, so the filter is invoked as

        cocor <commands> |&coco2msg | IDE message window

  This causes a redirection of the stderr instead of the stdout.  The
  &coco2msg.exe is used so the IDE finds the filter &coco2msg, but the real
  filter is coco2msg.exe
 
  Compile using the LARGE memory model.
*/
 
#include <dir.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <alloc.h>
#include <io.h>
#include <dos.h>
#include "filter.h"

#define TRUE  1
#define FALSE 0
 
char     CurFile[MAXPATH] ;
unsigned BufSize,CurBufLen;
char     *InBuffer,
         *OutBuffer,
         *CurInPtr,
         *CurOutPtr,
         *LinePtr;
char     Line[133];
long int InOff;
char     EndMark;
int      NoLines;
 
/************************************************************************
Function  : NextChar
Parameters: None
Returns   : next character in input buffer or 0 for end of file
 
Input from the standard input stream is buffered in a global buffer InBuffer
which is allocated in function main.  NextChar function will return
the next character in the buffer, reading from the input stream when the
buffer becomes empty.
************************************************************************/
char NextChar(void)
{
   if (CurInPtr < InBuffer+CurBufLen)   /* if buffer is not empty */
   {
      return *(CurInPtr++);             /* return next information */
  }
   else
   {
      CurInPtr = InBuffer;              /* reset pointer to front of buffer */
      lseek(0,InOff,0);                 /* seek to the next section for read */
      InOff += BufSize;                 /* increment pointer to next block */
      if ((CurBufLen = read(0,InBuffer,BufSize)) !=0)
         return NextChar();             /* recursive call returns first
                                           character in buffer after read */
      return 0;                         /* return 0 on end of file */
   }
}
 
/*************************************************************************
Function  : flushOut
Parameters: Size   The number of characters to be written out
Returns   : nothing

Strings to be sent to the message window are placed in a buffer called
OutBuffer.  A call to this function will write Size bytes to the
standard output stream and reset the output buffer pointer to the
beginning of the buffer.  Any additional information in the buffer is
thus lost.
**************************************************************************/
void flushOut(unsigned Size)
{
  if (Size != 0)                 /* don't flush an empty buffer */
  {
    CurOutPtr = OutBuffer;       /* reset pointer to beginning of buffer */
    lseek(1,0,2);                /* seek output stream to end */
    write(1,OutBuffer,Size);     /* write out Size bytes */
  }
}
 
/**************************************************************************
Function  : Put
Parameters: S     pointer to a string of characters
            Len   length of the string of characters
Returns   : Nothing.

Put places bytes into OutBuffer so they may be later flushed out into the
standard output stream using flushOut.
*************************************************************************/
void Put(char *S,int Len)
{
  int i;
 
  for (i = 0; i < Len; i++)
  {
    *CurOutPtr++ = S[i];                     /* place byte in buffer */
    if (CurOutPtr >= OutBuffer+BufSize)      /* if buffer overflows */
      flushOut(BufSize);                     /* flush to the stream */
  }
}
 
/**************************************************************************
Function  : ProcessLine
Parameters: Line   a pointer to the character line to be analyzed
Returns   : Nothing.
 
Filters lines output from cocor into a format usable in the Borland C++
environment message window.  Lines are simply sent straight through
with format characters for the message window.

Cocor Error Format: "filename", Line XXX, Col XXX : Message
**************************************************************************/
void ProcessLine(char *Line)
{
   static int HavePutFile = FALSE;
   char     Type;
   unsigned line,col;
   char     *s,*d;
   char     fn[MAXPATH];

/* don't try to process a NULL line */
   if (Line[0] == 0)
     return ;

   if (Line[0] == '*') {           /* Warning Line */
         if( !HavePutFile )  {
          Type = MsgNewFile;       /* indicate by sending type
                                      out to message window */
          *CurFile = '\0';
          Put(&Type,1);
          Put(CurFile,1);          /* along with null filename */
          HavePutFile = TRUE;
          }

      Type = MsgNewLine;           /* Fake line # etc.  */
      line = 32000;
      col = 1;
      Put(&Type,1);
      Put((char *)&line,2);
      Put((char *)&col,2);
      Put(Line,strlen(Line)+1);
      return ;
   }


  s = strchr(Line,'"');                     /* find "filename" */
  d = strchr(s+1,'"');
  if (d != NULL)                            /* if no "filename" : invalid line */
  {
     memmove(fn,s+1,(unsigned)(d-s-1));     /* save filename */
     fn[(unsigned)(d-s-1)] = 0;             /* null terminate name */
     memmove(Line,d+1,100);                 /* shift line left */
     if (strcmp(fn,CurFile) != 0)           /* if new filename */
     {
       Type = MsgNewFile;                   /* indicate by sending type
                                               out to message window */
       strcpy(CurFile,fn);
       Put(&Type,1);
       Put(CurFile,strlen(CurFile)+1);      /* along with the new name */
       HavePutFile = TRUE;
     }
     s = strchr(Line,'L');                  /* Find "Line" */
     memmove(Line,s+1,100);                 /* shift line left */
     s = strchr(Line,' ');                  /* Find " XXX" */
     memmove(Line,s+1,100);                 /* shift line left */

     s = strchr(Line,',');
     *s = 0;
     line = atoi(Line);                     /* if number is found convert string to integer */
     memmove(Line,s+1,100);                 /* shift line left */

     s = strchr(Line,'C');                  /* Find "Col" */
     memmove(Line,s+1,100);                 /* shift line left */
     s = strchr(Line,' ');                  /* Find " XXX" */
     memmove(Line,s+1,100);                 /* shift line left */
     s = strchr(Line,':');                  /* Find ":" */
     *s = 0;
     col = atoi(Line);                      /* if number is found convert string to integer */
     memmove(Line,s+1,100);                 /* shift line left */

     Type = MsgNewLine;                     /* set type to new line */
     Put(&Type,1);                          /* indicate need for new line */
     Put((char *)&line,2);                  /* put the number out */
     Put((char *)&col,2);                   /* tab over to put message */

     while (Line[0] == ' ' && Line[0] != 0) /* strip spaces from line */
       memmove(Line,&Line[1],strlen(Line));
     Put(Line,strlen(Line)+1);              /* output the message */
     return ;
  }

  if( !HavePutFile )
  {
        /* IDE expects the first message to
          be preceded by a filename.  Since
          we don't have one, fake it by
          sending a NULL file before the
          message.
        */
        Type = MsgNewFile;                  /* indicate by sending type
                                               out to message window */
        *CurFile = '\0';
        Put(&Type,1);
        Put(CurFile,1);                     /* along with null filename */
        HavePutFile = TRUE;
  }

      Type = MsgNewLine;                    /* Fake line # etc. */
      line    = 1;
      Put(&Type,1);
      Put((char *)&line,2);
      Put((char *)&line,2);
      while (Line[0] == ' ' && Line[0] != 0)
        memmove(Line,&Line[1],strlen(Line));
      Put(Line,strlen(Line)+1);
      return ;
}


/************************************************************************
Function  : Main

Returns   : zero on successful execution
          3 on an error condition

The main routine allocates memory for the input and output buffers.
Characters are then read from the input buffer building the line buffer
that will be sent to the filter processor.  Lines are read and filtered
until the end of input is reached.
************************************************************************/
int main(void)
{
  char c;
  int i, Type;
  unsigned long core;
 
  setmode(1,O_BINARY);               /* set standard out to binary mode */
  NoLines = FALSE;                   /* No lines have been read yet */
  core = farcoreleft();              /* get available memory */
  if (core > 64000U)                 /* limit buffers to total of 64000 */
    BufSize = 64000U;                /* bytes */
  else
    BufSize = (unsigned)core;
  if ((InBuffer = malloc(BufSize)) == NULL) /* allocate buffer space */
    exit(3);                         /* abort if error occured */
  CurInPtr = InBuffer;               /* split buffer */
  BufSize = BufSize/2;               /* between input and output buffers */
  OutBuffer = InBuffer + BufSize;
  CurOutPtr = OutBuffer;
  LinePtr = Line;                    /* set line buffer pointer */
  CurBufLen = 0;                     /* and reset buffer size to zero */
  Put(PipeId,PipeIdLen);             /* Identify process to message window */

  while ((c = NextChar()) != 0)      /* read characters */
  {
    if ((c == 13) || (c == 10))      /* build line until new line is seen */
    {
      *LinePtr = 0;
      ProcessLine(Line);             /* then filter the line */
      LinePtr = Line;
    }
    /* characters are added to line only up to 132 characters */
    else if ((FP_OFF(LinePtr) - FP_OFF(&Line)) < 132)
    {
      *LinePtr = c;
      LinePtr++;
      }
  }
   *LinePtr = 0;
   ProcessLine(Line);                /* filter last line */
   if (NoLines)                      /* if no lines */
   {
      Type = MsgNewLine;             /* send something to the */
      i = 1;                         /* message window */
      Put((char *)&Type,1);
      Put((char *)&i,2);
      Put((char *)&i,2);
      Put(" ",2);
  }
   EndMark = MsgEoFile;              /* indicate end of input to */
   Put(&EndMark,1);                  /* message window */
   flushOut((unsigned)(CurOutPtr-OutBuffer));  /* flush out remaining buffer */
 
   return  0;                        /* everything went ok */
}
