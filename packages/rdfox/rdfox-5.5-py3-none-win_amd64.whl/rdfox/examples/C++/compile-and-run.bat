cl /EHsc /W3 /WX /MT /I "..\..\include" CppRDFoxDemo.cpp libRDFox.lib /link /LIBPATH:"..\..\lib"
copy ..\..\lib\libRDFox.dll .
xcopy /s ..\data .
.\CppRDFoxDemo.exe
        