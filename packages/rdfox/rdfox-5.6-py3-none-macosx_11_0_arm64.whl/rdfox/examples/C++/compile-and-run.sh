#!/usr/bin/env bash
g++ -Wall -Werror -std=gnu++11 CppRDFoxDemo.cpp -o CppRDFoxDemo -I../../include -lRDFox -L../../lib
cp ../data/* .
LD_LIBRARY_PATH=../../lib ./CppRDFoxDemo
        