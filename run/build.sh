#!/bin/bash

export CPLUS_INCLUDE_PATH=\
$PWD/src:\
$PWD/src/cli/include/HTTPRequest:\
$PWD/src/cli/include/HTTPRequest/include;

g++ -std=c++20 $PWD/src/cli/*.cpp -o $PWD/bin/mana.64;

