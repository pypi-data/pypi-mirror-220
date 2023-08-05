cl /EHsc /W3 /WX /MT /I "..\..\include" CRDFoxDemo.c libRDFox.lib /link /LIBPATH:"..\..\lib"
copy ..\..\lib\libRDFox.dll .
xcopy /s ..\data .
.\CRDFoxDemo.exe
        