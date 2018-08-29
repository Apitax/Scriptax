#!/usr/bin/env bash
java -jar antlr-4.7.1-complete.jar -o build -listener -visitor -Dlanguage=Python3 src/Ah3.g4