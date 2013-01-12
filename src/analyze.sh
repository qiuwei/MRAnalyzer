#!/bin/sh

dirname=$1
for filename in $(find $1 -name '*.rcft')
do
    java -jar erca.jar rcfhtml --rcft $filename ${filename%.rcft}.rcf.html
    java -jar erca.jar clfbuild --rcft $filename ${filename%.rcft}.rcf.xmi ${filename%.rcft}.clf.xmi
    java -jar erca.jar clfdot ${filename%.rcft}.clf.xmi ${filename%.rcft}.clf.dot 
    dot -Tps ${filename%.rcft}.clf.dot -o ${filename%.rcft}.clf.ps
done
