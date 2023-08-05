#!/usr/bin/env bash
gcc -Wall -Werror CRDFoxDemo.c -o CRDFoxDemo -I../../include -lRDFox -L../../lib
cp ../data/* .
LD_LIBRARY_PATH=../../lib ./CRDFoxDemo
        