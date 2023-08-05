The distribution of RDFox consists of the following files and directories:

- 'RDFox' (macOS/Linux) or 'RDFox.exe' (Windows): a stand-alone executable that can be used to run RDFox on the
  command line.

- 'lib': a directory containing the following libraries:

  * 'JRDFox.jar': the Java bridge to the native RDFox engine.
  
  * 'libRDFox.dylib' (macOS), 'libRDFox.so' (Linux), or 'libRDFox.dll' (Windows): a dynamic library that implements
    the native methods of JRDFox.

  * 'libRDFox.lib' (Windows only): the import library needed for linking 'libRDFox.dll' on Windows.

- 'include': a directory containing definitions for an EXPERIMENTAL C API. The definitions include C++ classes that
  can be used to make it easier to correctly manage the resources exposed by the C API within C++ applications.

- 'examples': a directory containing demonstration programs that show how to call RDFox as a library.

  * 'C': a directory containing a C source file demonstrating how to call RDFox via the experimental C API and a script
    ('compile-and-run.sh' on macOS and Linux, 'compile-and-run.bat' on Windows) to build and run the demo. On macOS and
    Linux, the script assumes a C-99 compliant version of gcc is available on the path. On Windows, the script assumes
    that 'vcvars64.bat' has been executed in the shell prior to execution.

  * 'C++': a directory containing a C++ source file demonstrating how to call RDFox via the C++ wrapper for the
    experimental C API and a script ('compile-and-run.sh' on macOS and Linux, 'compile-and-run.bat' on Windows) to
    build and run the demo. On macOS and Linux, the script assumes a version of g++ supporting C++11 is available on the
    path. On Windows, the script assumes that 'vcvars64.bat' has been executed in the shell prior to execution.

  * 'Java': a directory containing source code for a program demonstrating how to call RDFox via the JRDFox API.
    The 'examples/Java/build.xml' Apache Ant script can be used to compile and run the program.

To use JRDFox in your project, simply add JRDFox.jar to your classpath, and make sure that the path to the
dynamic library is correctly specified  when starting your program using the following JVM option:

    -Djava.library.path=<path>
